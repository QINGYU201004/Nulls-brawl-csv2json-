import csv
import json
import os
import time
import glob
from collections import defaultdict
from tqdm import tqdm

def load_config(config_file="config.json"):
    """从JSON文件加载配置"""
    if not os.path.exists(config_file):
        print(f"错误: 配置文件 {config_file} 不存在")
        return None
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            print(f"已加载配置文件: {config_file}")
            return config
    except Exception as e:
        print(f"加载配置文件出错: {str(e)}")
        return None

def clean_csv_value(value):
    """清理CSV值，保留空白字段为空"""
    if not isinstance(value, str):
        return value
    
    # 处理空值情况 - 直接保留为空
    if not value or value in ['""', '""""']:
        return ""
    
    # 简单去除首尾双引号
    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    
    # 处理连续双引号
    return value.replace('""', '"')

def convert_value(value, data_type):
    """根据数据类型转换值"""
    try:
        if data_type == 'int':
            return int(value)
        elif data_type == 'float':
            return float(value)
        elif data_type == 'bool':
            # 布尔类型转换
            if isinstance(value, str):
                if value.lower() in ['true', 'yes', '1']:
                    return True
                elif value.lower() in ['false', 'no', '0']:
                    return False
            return value  # 无法转换则返回原值
        else:  # string或其他类型
            return value  # 直接返回原值
    except (ValueError, AttributeError):
        # 转换失败时返回原值
        return value

def find_matching_files(config):
    """根据配置查找匹配的文件对"""
    base_path = config.get("data_folder", ".")
    pattern = config.get("csv_pattern", "*2.csv")
    
    # 查找所有修改版文件
    modified_files = glob.glob(os.path.join(base_path, pattern))
    
    pairs = []
    
    for modified_file in modified_files:
        # 获取文件名
        filename = os.path.basename(modified_file)
        
        # 检查是否是修改版文件 (文件名以 "2.csv" 结尾)
        if filename.endswith("2.csv"):
            # 直接替换"2.csv"为".csv"获取原版文件名
            original_name = filename.replace("2.csv", ".csv")
            original_file = os.path.join(base_path, original_name)
            
            # 检查原版文件是否存在
            if os.path.exists(original_file):
                # 确定JSON键名 (使用原始文件名)
                json_key = os.path.splitext(original_name)[0]
                pairs.append((original_file, modified_file, json_key))
            else:
                print(f"警告: 未找到原版文件 {original_file}")
        else:
            print(f"警告: 忽略不匹配的文件 {filename}")
    
    return pairs

def extract_nested_values(file_path, key_field):
    """从CSV文件中提取嵌套值结构"""
    result = {}
    current_key = None
    current_nested = defaultdict(list)
    
    print(f"  开始提取CSV文件: {os.path.basename(file_path)}")
    start_time = time.time()
    
    try:
        # 获取文件大小
        file_size = os.path.getsize(file_path)
        print(f"  文件大小: {file_size/(1024*1024):.2f} MB")
        
        # 统计行数
        with open(file_path, 'r', encoding='utf-8') as f:
            # 跳过标题行和类型行
            next(f)  # 标题行
            next(f)  # 类型行
            line_count = sum(1 for _ in f)
        
        print(f"  总行数: {line_count}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            # 读取标题行
            header_line = next(f)
            header = [col.strip('"') for col in next(csv.reader([header_line]))]
            
            # 读取类型行
            type_line = next(f)
            type_list = [t.strip() for t in next(csv.reader([type_line]))]
            
            # 创建字段类型映射
            field_types = dict(zip(header, type_list))
            
            # 使用tqdm显示实时进度条
            reader = csv.DictReader(f, fieldnames=header)
            pbar = tqdm(total=line_count, desc="提取进度", unit="行")
            
            for row in reader:
                # 清理字段值 - 保留空白字段为空
                cleaned_row = {}
                for k, v in row.items():
                    cleaned_value = clean_csv_value(v)
                    if cleaned_value != "":  # 只保留非空值
                        # 获取字段类型并转换值
                        data_type = field_types.get(k, 'string')
                        converted_value = convert_value(cleaned_value, data_type)
                        cleaned_row[k] = converted_value
                
                # 检查关键字段是否存在
                if key_field in cleaned_row and cleaned_row[key_field] != "":
                    # 保存当前嵌套结构
                    if current_key and current_nested:
                        result[current_key] = dict(current_nested)
                    
                    # 开始新嵌套结构
                    current_key = cleaned_row[key_field]
                    current_nested = defaultdict(list)
                    
                    # 添加当前行数据到嵌套结构
                    for field, value in cleaned_row.items():
                        if field != key_field:
                            current_nested[field].append(value)
                else:
                    # 添加值到当前嵌套结构
                    for field, value in cleaned_row.items():
                        if value != "":
                            current_nested[field].append(value)
                
                pbar.update(1)  # 更新进度条
            
            # 保存最后一个嵌套结构
            if current_key and current_nested:
                result[current_key] = dict(current_nested)
            
            pbar.close()  # 关闭进度条
        
        elapsed = time.time() - start_time
        print(f"  提取完成: {len(result)} 个嵌套对象, 耗时: {elapsed:.2f}秒")
        return result
    
    except Exception as e:
        print(f"  读取文件出错: {str(e)}")
        return {}

def compare_nested_values(original_csv, modified_csv, key_field):
    """比较两个CSV文件的嵌套值结构"""
    print(f"  开始比较嵌套值结构...")
    start_time = time.time()
    
    try:
        # 提取原版CSV的嵌套值
        orig_nested = extract_nested_values(original_csv, key_field)
        
        # 提取更改版CSV的嵌套值
        mod_nested = extract_nested_values(modified_csv, key_field)
        
        # 准备结果结构
        changes = {}
        
        # 检测修改和新对象
        new_count = 0
        mod_count = 0
        
        # 使用进度条处理修改版嵌套数据
        for key, mod_data in tqdm(mod_nested.items(), desc="检测嵌套修改", unit="对象"):
            # 新建对象处理
            if key not in orig_nested:
                changes[key] = mod_data
                new_count += 1
            else:
                # 修改对象处理
                orig_data = orig_nested[key]
                changed_fields = {}
                
                # 检查所有字段
                for field, mod_values in mod_data.items():
                    # 新字段处理
                    if field not in orig_data:
                        changed_fields[field] = mod_values
                        mod_count += 1
                    else:
                        # 修改字段处理
                        orig_values = orig_data[field]
                        
                        # 检查值是否相同
                        if mod_values != orig_values:
                            changed_fields[field] = mod_values
                            mod_count += 1
                
                if changed_fields:
                    changes[key] = changed_fields
        
        elapsed = time.time() - start_time
        print(f"  比较完成: 发现 {len(changes)} 处修改 ({new_count} 项新建, {mod_count} 项修改), 耗时: {elapsed:.2f}秒")
        return changes
    
    except Exception as e:
        print(f"  比较文件出错: {str(e)}")
        return {}

def validate_numeric_fields(data, config):
    """验证数字字段，确保只包含数字值"""
    if not data:
        return
    
    # 从配置获取数字字段列表
    numeric_fields = set(config.get("numeric_fields", []))
    
    for section, content in data.items():
        if isinstance(content, dict):
            for key, value in content.items():
                # 检查字段名是否暗示数字类型
                if key.lower() in numeric_fields:
                    # 处理列表值
                    if isinstance(value, list):
                        for i, item in enumerate(value):
                            if not isinstance(item, (int, float)) and not str(item).isdigit():
                                print(f"警告: 字段 '{key}' 应为数字，但值为 '{item}'，已设置为0")
                                value[i] = 0
                    # 处理单个值
                    elif not isinstance(value, (int, float)) and not str(value).isdigit():
                        print(f"警告: 字段 '{key}' 应为数字，但值为 '{value}'，已设置为0")
                        content[key] = 0

def fix_problem_values(data, config):
    """根据配置修复问题值"""
    if not data:
        return
    
    # 从配置获取问题值设置
    problem_values = config.get("problem_values", {})
    
    for problem_value, settings in problem_values.items():
        target_fields = set(settings.get("fields", []))
        replace_with = settings.get("replace_with", 0)
        
        for section, content in data.items():
            if isinstance(content, dict):
                for key, value in content.items():
                    # 检查值是否包含问题值
                    if isinstance(value, str) and problem_value in value:
                        # 如果字段在目标字段中
                        if key.lower() in target_fields:
                            print(f"修复: 字段 '{key}' 的值 '{value}' 替换为 {replace_with}")
                            content[key] = replace_with
                    # 处理列表值
                    elif isinstance(value, list):
                        for i, item in enumerate(value):
                            if isinstance(item, str) and problem_value in item:
                                if key.lower() in target_fields:
                                    print(f"修复: 字段 '{key}' 的值 '{item}' 替换为 {replace_with}")
                                    value[i] = replace_with

def generate_combined_mod(csv_pairs, config):
    """
    生成合并的模组JSON文件 - 自动处理所有匹配的CSV文件对
    """
    mod_metadata = config.get("mod_metadata", {})
    key_field = config.get("key_field", "Name")
    output_file = config.get("output_file", "content.json")
    
    total_start = time.time()
    print(f"\n开始生成模组: {mod_metadata.get('title', '综合修改模组')}")
    
    # 构建模组结构
    combined_mod = {
        "@title": mod_metadata.get("title", "综合修改模组"),
        "@description": mod_metadata.get("description", {"CN": "自动生成的综合修改模组"}),
        "@author": mod_metadata.get("author", "自动生成"),
        "@gv": mod_metadata.get("gv", 1)
    }
    
    # 处理所有CSV对
    processed_count = 0
    skipped_count = 0
    
    for original_csv, modified_csv, json_key in csv_pairs:
        # 检查文件是否存在
        if not os.path.exists(original_csv):
            print(f"\n跳过: 原版CSV文件不存在 - {original_csv}")
            skipped_count += 1
            continue
        if not os.path.exists(modified_csv):
            print(f"\n跳过: 更改版CSV文件不存在 - {modified_csv}")
            skipped_count += 1
            continue
            
        print(f"\n处理: {os.path.basename(original_csv)} -> {os.path.basename(modified_csv)}")
        print(f"关键字段: {key_field}")
        
        pair_start = time.time()
        changes = compare_nested_values(original_csv, modified_csv, key_field)
        pair_elapsed = time.time() - pair_start
        
        if changes:
            # 修复特定问题值
            fix_problem_values(changes, config)
            
            # 验证数字字段
            validate_numeric_fields(changes, config)
            
            # 直接使用原始结构
            combined_mod[json_key] = changes
            
            print(f"  处理完成: 找到 {len(changes)} 处修改, 耗时: {pair_elapsed:.2f}秒")
            processed_count += 1
        else:
            print(f"  未发现修改, 耗时: {pair_elapsed:.2f}秒")
            processed_count += 1
    
    # 写入JSON文件
    print(f"\n正在写入JSON文件: {output_file}")
    write_start = time.time()
    
    try:
        # 使用进度条显示写入进度
        with tqdm(total=1, desc="写入JSON文件") as pbar:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(combined_mod, f, ensure_ascii=False, indent=2)
            pbar.update(1)
        
        write_elapsed = time.time() - write_start
        
        total_elapsed = time.time() - total_start
        print(f"\n已生成模组文件: {output_file}")
        print(f"处理统计: {processed_count} 个文件对已处理, {skipped_count} 个文件对被跳过")
        print(f"JSON写入耗时: {write_elapsed:.2f}秒")
        print(f"总处理时间: {total_elapsed:.2f}秒")
        
        # 计算平均处理速度
        total_size = sum(os.path.getsize(csv[0]) for csv in csv_pairs if os.path.exists(csv[0]))
        if total_size > 0:
            print(f"平均处理速度: {total_size/(total_elapsed*1024*1024):.2f} MB/s")
        else:
            print("平均处理速度: 没有可处理的文件")
        
        return combined_mod
    
    except Exception as e:
        print(f"写入JSON文件出错: {str(e)}")
        return None

# 主入口
if __name__ == "__main__":
    # 加载配置文件
    config = load_config()
    if not config:
        print("无法加载配置，使用默认设置")
        config = {
            "mod_metadata": {
                "title": "默认模组",
                "description": {"CN": "自动生成的默认模组"},
                "author": "自动生成",
                "gv": 1
            },
            "key_field": "Name",
            "data_folder": ".",
            "csv_pattern": "*2.csv",
            "output_file": "content.json",
            "numeric_fields": [
                "scale", "size", "count", "value", "number", "level", "speed", "damage"
            ],
            "problem_values": {
                "cam_bone": {
                    "fields": ["scale", "size", "count", "value", "number"],
                    "replace_with": 0
                }
            }
        }
    
    # 自动查找所有匹配的CSV文件对
    csv_pairs = find_matching_files(config)
    
    if not csv_pairs:
        data_folder = config.get("data_folder", ".")
        print("警告: 未找到任何匹配的CSV文件对")
        print("请确保您的修改版CSV文件名以 '2.csv' 结尾")
        print("例如: skins2.csv, animations2.csv")
        print(f"目录 {data_folder} 中的文件:")
        for f in os.listdir(data_folder):
            if f.endswith(".csv"):
                print(f"  - {f}")
        exit(1)
    
    print(f"找到 {len(csv_pairs)} 个CSV文件对:")
    for original, modified, json_key in csv_pairs:
        print(f"  - {os.path.basename(original)} -> {os.path.basename(modified)} -> {json_key}")
    
    # 生成合并模组
    generate_combined_mod(csv_pairs, config)
