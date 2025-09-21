import os
import sys
from pathlib import Path
import shutil
from lib.csv_to_json import load_config, find_matching_files, generate_combined_mod
from lib.csv_clean import compare_csv_headers, add_missing_columns
from lib.csv_compression import decompress_csv, compress_csv
from lib.json_merge import json_merge_ui

# 定义颜色代码
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'

# 清屏并全屏显示
def clear_screen():
    # 跨平台清屏
    os.system('cls' if os.name == 'nt' else 'clear')

# 创建所有目录结构
def create_all_folders():
    # CSV 目录结构
    from lib.csv_compression import create_csv_folders
    create_csv_folders()
    
    # 创建日志目录
    log_dir = Path("Logs")
    log_dir.mkdir(exist_ok=True)
    
    # 创建CSV清理目录
    clean_dir = Path("CSV") / "CSV_CLEAN"
    clean_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建CSV添加列目录
    added_dir = Path("CSV") / "CSV_ADDED"
    added_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建JSON合并目录
    json_merged_dir = Path("JSON_MERGED")
    json_merged_dir.mkdir(exist_ok=True)
    
    return True

# 显示目录状态
def show_folder_status():
    clear_screen()
    
    # 获取终端宽度
    terminal_size = shutil.get_terminal_size()
    width = terminal_size.columns
    
    print("\n" + "=" * width)
    print(f"{GREEN}清雨制作｜多功能CSV数据处理工具 v2.0{RESET}".center(width))
    print("=" * width)
    print("\n目录状态:")
    
    # CSV 目录
    print("[CSV]")
    csv_dirs = [
        "In-Compressed", "In-Decompressed", 
        "Out-Compressed", "Out-Decompressed",
        "CSV_CLEAN", "CSV_ADDED"
    ]
    for dir_name in csv_dirs:
        dir_path = Path("CSV") / dir_name
        file_count = len(list(dir_path.glob("*"))) if dir_path.exists() else 0
        status = f"存在 ({file_count}个文件)" if dir_path.exists() else "不存在"
        print(f"  - {dir_name}: {status}")
    
    # 日志目录
    log_dir = Path("Logs")
    log_count = len(list(log_dir.glob("*.log"))) if log_dir.exists() else 0
    status = f"存在 ({log_count}个日志)" if log_dir.exists() else "不存在"
    print("\n[日志]")
    print(f"  - Logs: {status}")
    
    # JSON合并目录
    json_merged_dir = Path("JSON_MERGED")
    json_count = len(list(json_merged_dir.glob("*.json"))) if json_merged_dir.exists() else 0
    status = f"存在 ({json_count}个文件)" if json_merged_dir.exists() else "不存在"
    print("\n[JSON]")
    print(f"  - JSON_MERGED: {status}")
    
    print("\n" + "=" * width)
    input(f"{GREEN}按回车键返回主菜单...{RESET}")

# 主入口
if __name__ == "__main__":
    # 创建所有目录
    create_all_folders()
    
    while True:  # 主循环
        # 获取终端宽度
        terminal_size = shutil.get_terminal_size()
        width = terminal_size.columns
        
        # 清屏并显示全屏顶头菜单
        clear_screen()
        
        # 显示功能选择菜单
        print("=" * width)
        print(f"{GREEN}清雨制作｜多功能CSV数据处理工具 v2.0{RESET}".center(width))
        print("=" * width)
        print("\n请选择功能:")
        print("1: 自动将CSV转为模组JSON")
        print("2: 查询CSV表头差异并清理多余列")
        print("3: 查询CSV表头差异并添加缺失列")
        print("4: 解压CSV文件")
        print("5: 压缩CSV文件")
        print("6: 合并JSON文件")
        print("7: 查看目录状态")  # 移到底部
        print("\n" + "=" * width)
        print("0: 退出程序")
        print("=" * width)
        
        choice = input("\n请输入选项 (0-7): ").strip()
        
        if choice == "1":
            clear_screen()
            print("=" * width)
            print(f"{GREEN}自动将CSV转为模组JSON{RESET}".center(width))
            print("=" * width)
            
            # 加载配置文件
            config = load_config()
            if not config:
                print("无法加载配置，请检查配置文件是否存在且格式正确")
                input(f"{GREEN}\n按回车键继续...{RESET}")
                continue  # 返回主菜单
            
            # 自动查找所有匹配的CSV文件对
            csv_pairs = find_matching_files(config)
            
            if not csv_pairs:
                data_folder = config.get("data_folder", ".")
                print("警告: 未找到任何匹配的CSV文件对")
                print(f"请检查配置文件中的 csv_pattern: {config.get('csv_pattern', '*2.csv')}")
                print(f"目录 {data_folder} 中的文件:")
                for f in os.listdir(data_folder):
                    if f.endswith(".csv"):
                        print(f"  - {f}")
                input(f"{GREEN}\n按回车键返回主菜单...{RESET}")
                continue  # 继续循环而不是退出
            
            print(f"找到 {len(csv_pairs)} 个CSV文件对:")
            for original, modified, json_key in csv_pairs:
                print(f"  - {os.path.basename(original)} -> {os.path.basename(modified)} -> {json_key}")
            
            # 生成合并模组
            generate_combined_mod(csv_pairs, config)
            
            # 操作完成后等待用户按回车继续
            print("\n" + "=" * width)
            input(f"{GREEN}\n操作完成，按回车键返回主菜单...{RESET}")
        
        elif choice == "2":
            clear_screen()
            print("=" * width)
            print(f"{GREEN}查询CSV表头差异并清理多余列{RESET}".center(width))
            print("=" * width)
            
            # 查询CSV表头差异
            data_folder = input("请输入CSV文件所在目录 (默认为当前目录): ").strip() or "."
            
            # 获取目录中的CSV文件
            csv_files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]
            if not csv_files:
                print(f"目录 {data_folder} 中没有CSV文件")
                print("\n" + "=" * width)
                input(f"{GREEN}\n按回车键返回主菜单...{RESET}")
                continue
            
            # 显示文件列表
            print("\n可用的CSV文件:")
            for i, f in enumerate(csv_files, 1):
                print(f"{i}: {f}")
            
            # 选择原始文件
            try:
                orig_idx = int(input("\n请选择原始文件编号: ")) - 1
                if orig_idx < 0 or orig_idx >= len(csv_files):
                    raise ValueError
            except ValueError:
                print("无效的选择")
                print("\n" + "=" * width)
                input(f"{GREEN}\n按回车键返回主菜单...{RESET}")
                continue
            
            # 选择修改文件
            try:
                mod_idx = int(input("请选择修改文件编号: ")) - 1
                if mod_idx < 0 or mod_idx >= len(csv_files):
                    raise ValueError
            except ValueError:
                print("无效的选择")
                print("\n" + "=" * width)
                input(f"{GREEN}\n按回车键返回主菜单...{RESET}")
                continue
            
            # 获取完整路径
            original_csv = os.path.join(data_folder, csv_files[orig_idx])
            modified_csv = os.path.join(data_folder, csv_files[mod_idx])
            
            # 比较表头并清理多余列
            compare_csv_headers(original_csv, modified_csv)
            
            # 操作完成后等待用户按回车继续
            print("\n" + "=" * width)
            input(f"{GREEN}\n操作完成，按回车键返回主菜单...{RESET}")
        
        elif choice == "3":
            clear_screen()
            print("=" * width)
            print(f"{GREEN}查询CSV表头差异并添加缺失列{RESET}".center(width))
            print("=" * width)
            
            # 查询CSV表头差异
            data_folder = input("请输入CSV文件所在目录 (默认为当前目录): ").strip() or "."
            
            # 获取目录中的CSV文件
            csv_files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]
            if not csv_files:
                print(f"目录 {data_folder} 中没有CSV文件")
                print("\n" + "=" * width)
                input(f"{GREEN}\n按回车键返回主菜单...{RESET}")
                continue
            
            # 显示文件列表
            print("\n可用的CSV文件:")
            for i, f in enumerate(csv_files, 1):
                print(f"{i}: {f}")
            
            # 选择原始文件
            try:
                orig_idx = int(input("\n请选择原始文件编号: ")) - 1
                if orig_idx < 0 or orig_idx >= len(csv_files):
                    raise ValueError
            except ValueError:
                print("无效的选择")
                print("\n" + "=" * width)
                input(f"{GREEN}\n按回车键返回主菜单...{RESET}")
                continue
            
            # 选择修改文件
            try:
                mod_idx = int(input("请选择修改文件编号: ")) - 1
                if mod_idx < 0 or mod_idx >= len(csv_files):
                    raise ValueError
            except ValueError:
                print("无效的选择")
                print("\n" + "=" * width)
                input(f"{GREEN}\n按回车键返回主菜单...{RESET}")
                continue
            
            # 获取完整路径
            original_csv = os.path.join(data_folder, csv_files[orig_idx])
            modified_csv = os.path.join(data_folder, csv_files[mod_idx])
            
            # 比较表头并添加缺失列
            add_missing_columns(original_csv, modified_csv)
            
            # 操作完成后等待用户按回车继续
            print("\n" + "=" * width)
            input(f"{GREEN}\n操作完成，按回车键返回主菜单...{RESET}")
        
        elif choice == "4":
            clear_screen()
            print("=" * width)
            print(f"{GREEN}解压CSV文件{RESET}".center(width))
            print("=" * width)
            
            print("开始解压CSV文件...")
            if decompress_csv():
                print("解压操作完成！")
            else:
                print("解压过程中出现问题")
            
            print("\n" + "=" * width)
            input(f"{GREEN}\n按回车键返回主菜单...{RESET}")
        
        elif choice == "5":
            clear_screen()
            print("=" * width)
            print(f"{GREEN}压缩CSV文件{RESET}".center(width))
            print("=" * width)
            
            print("开始压缩CSV文件...")
            if compress_csv():
                print("压缩操作完成！")
            else:
                print("压缩过程中出现问题")
            
            print("\n" + "=" * width)
            input(f"{GREEN}\n按回车键返回主菜单...{RESET}")
        
        elif choice == "6":  # JSON合并功能
            clear_screen()
            print("=" * width)
            print(f"{GREEN}合并JSON文件{RESET}".center(width))
            print("=" * width)
            
            # 执行JSON合并
            if json_merge_ui():
                print("JSON合并完成！")
            else:
                print("JSON合并过程中出现问题")
            
            # 操作完成后等待用户按回车继续
            print("\n" + "=" * width)
            input(f"{GREEN}\n操作完成，按回车键返回主菜单...{RESET}")
        
        elif choice == "7":  # 目录状态功能（移到底部）
            show_folder_status()
        
        elif choice == "0":
            clear_screen()
            print("=" * width)
            print(f"{GREEN}程序已退出{RESET}".center(width))
            print("=" * width)
            break  # 退出循环
        
        else:
            print("无效选项，请重新选择")
            input(f"{GREEN}\n按回车键继续...{RESET}")
            continue
