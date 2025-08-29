import csv
import json
import os
import time
from collections import defaultdict
from tqdm import tqdm

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

def validate_numeric_fields(data):
    """验证数字字段，确保只包含数字值"""
    # 定义可能为数字的字段名
    numeric_fields = {'scale', 'size', 'count', 'value', 'number', 'level', 'speed', 'damage'}
    
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

def fix_cam_bone_value(data):
    """修复cam_bone值问题"""
    for section, content in data.items():
        if isinstance(content, dict):
            for key, value in content.items():
                # 检查值是否包含"cam_bone"
                if isinstance(value, str) and "cam_bone" in value:
                    # 如果字段应该是数字，设置为0
                    if key.lower() in {'scale', 'size', 'count', 'value', 'number'}:
                        print(f"修复: 字段 '{key}' 的值 '{value}' 替换为0")
                        content[key] = 0
                # 处理列表值
                elif isinstance(value, list):
                    for i, item in enumerate(value):
                        if isinstance(item, str) and "cam_bone" in item:
                            if key.lower() in {'scale', 'size', 'count', 'value', 'number'}:
                                print(f"修复: 字段 '{key}' 的值 '{item}' 替换为0")
                                value[i] = 0

def generate_combined_mod(csv_pairs, mod_metadata, key_field):
    """
    生成合并的模组JSON文件 - 原始结构版
    """
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
    for csv_pair in csv_pairs:
        if len(csv_pairs) == 0:
            print("没有配置CSV文件对")
            continue
            
        if len(csv_pair) < 3:
            print(f"配置错误: {csv_pair} (需要3个元素: 原版CSV, 更改版CSV, JSON键名)")
            continue
            
        original_csv, modified_csv, json_key = csv_pair[:3]
        
        if not os.path.exists(original_csv):
            print(f"警告: 原版CSV文件不存在 - {original_csv}")
            continue
        if not os.path.exists(modified_csv):
            print(f"警告: 更改版CSV文件不存在 - {modified_csv}")
            continue
            
        print(f"\n处理: {os.path.basename(original_csv)} -> {os.path.basename(modified_csv)}")
        print(f"关键字段: {key_field}")
        
        pair_start = time.time()
        changes = compare_nested_values(original_csv, modified_csv, key_field)
        pair_elapsed = time.time() - pair_start
        
        if changes:
            # 修复特定问题
            fix_cam_bone_value(changes)
            
            # 验证数字字段
            validate_numeric_fields(changes)
            
            # 直接使用原始结构
            combined_mod[json_key] = changes
            
            print(f"  处理完成: 找到 {len(changes)} 处修改, 耗时: {pair_elapsed:.2f}秒")
        else:
            print(f"  未发现修改, 耗时: {pair_elapsed:.2f}秒")
    
    # 写入JSON文件
    output_file = "content.json"
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
        print(f"JSON写入耗时: {write_elapsed:.2f}秒")
        print(f"总处理时间: {total_elapsed:.2f}秒")
        
        # 计算平均处理速度
        total_size = sum(os.path.getsize(csv[0]) for csv in csv_pairs)
        print(f"平均处理速度: {total_size/(total_elapsed*1024*1024):.2f} MB/s")
        
        return combined_mod
    
    except Exception as e:
        print(f"写入JSON文件出错: {str(e)}")
        return None

# 使用示例
if __name__ == "__main__":
    # 配置模组元数据
    mod_metadata = {
        "title": "模组名",
        "description": {
            "EN": "English",
            "CN": "中文"
        },
        "author": "清雨（QQ：3384853402）",
        "gv": 62
    }
    
    # 配置要处理的CSV文件对
    # 格式: (原版CSV, 更改版CSV, JSON键名)
    csv_pairs = [
        ("skins.csv", "skins2.csv", "skins"),
        ("skin_confs.csv", "skin_confs2.csv", "skin_confs"),
        ("skin_campaigns.csv", "skin_campaigns2.csv", "skin_campaigns"),
        ("animations.csv", "animations2.csv", "animations"),
        ("faces.csv", "faces2.csv", "faces"),
        ("area_effects.csv", "area_effects2.csv", "area_effects"),
        ("effects.csv", "effects2.csv", "effects"),
        ("projectiles.csv", "projectiles2.csv", "projectiles"),
        ("sounds.csv", "sounds2.csv", "sounds"),
        ("skills.csv", "skills2.csv", "skills"),
        #("emotes.csv", "emotes2.csv", "emotes"),
    ]
    
    # 配置关键字段
    key_field = "Name"  # 关键字段
    
    # 生成合并模组
    generate_combined_mod(csv_pairs, mod_metadata, key_field)
