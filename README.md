# Null's Brawl CSV to JSON Mod Generator



[English](#english) | [中文](#中文) | [Русский](#русский)

---

<a name="english"></a>
## 🚀 English Guide

📥 Installation

Clone the repository:

git clone https://github.com/QINGYU201004/Nulls-brawl-csv2json-.git cd Nulls-brawl-csv2json- 

Install dependencies:

pip install -r requirements.txt 

🛠️ Configuration

Edit config.json:

{ "mod_metadata": { "title": "Your Mod Name", "description": { "EN": "English mod description", "CN": "中文模组描述", "RU": "Описание мода на русском" }, "author": "Your Name", "gv": 62 }, "key_field": "Name", "data_folder": "examples", "csv_pattern": "*2.csv", "output_file": "content.json", "numeric_fields": [ "scale", "size", "count", "value" ], "problem_values": { "cam_bone": { "fields": ["scale", "size"], "replace_with": 0 } } } 

📂 File Preparation

Create your CSV files:

Original files: filename.csv

Modified files: filename2.csv

Place files in the examples directory:

Nulls-brawl-csv2json-/ ├── examples/ │ ├── characters.csv # Original file │ ├── characters2.csv # Modified file │ ├── abilities.csv # Original file │ └── abilities2.csv # Modified file 

▶️ Running the Script

python main.py 

📊 Output

The generated mod file will be saved as content.json in the project root.

<a name="中文"></a>
## 🚀 中文指南

📥 安装

克隆仓库:

git clone https://github.com/QINGYU201004/Nulls-brawl-csv2json-.git cd Nulls-brawl-csv2json- 

安装依赖:

pip install -r requirements.txt 

🛠️ 配置

编辑 config.json:

{ "mod_metadata": { "title": "您的模组名称", "description": { "EN": "English mod description", "CN": "中文模组描述", "RU": "Описание мода на русском" }, "author": "您的名称", "gv": 62 }, "key_field": "Name", "data_folder": "examples", "csv_pattern": "*2.csv", "output_file": "content.json", "numeric_fields": [ "scale", "size", "count", "value" ], "problem_values": { "cam_bone": { "fields": ["scale", "size"], "replace_with": 0 } } } 

📂 文件准备

创建CSV文件:

原版文件: filename.csv

修改版文件: filename2.csv

将文件放入 examples 目录:

Nulls-brawl-csv2json-/ ├── examples/ │ ├── 角色.csv # 原版文件 │ ├── 角色2.csv # 修改版文件 │ ├── 技能.csv # 原版文件 │ └── 技能2.csv # 修改版文件 

▶️ 运行脚本

python main.py 

📊 输出

生成的模组文件将保存为项目根目录下的 content.json

<a name="русский"></a>
## 🚀 Русское руководство

📥 Установка

Клонируйте репозиторий:

git clone https://github.com/QINGYU201004/Nulls-brawl-csv2json-.git cd Nulls-brawl-csv2json- 

Установите зависимости:

pip install -r requirements.txt 

🛠️ Настройка

Отредактируйте config.json:

{ "mod_metadata": { "title": "Название вашего мода", "description": { "EN": "English mod description", "CN": "中文模组描述", "RU": "Описание мода на русском" }, "author": "Ваше имя", "gv": 62 }, "key_field": "Name", "data_folder": "examples", "csv_pattern": "*2.csv", "output_file": "content.json", "numeric_fields": [ "scale", "size", "count", "value" ], "problem_values": { "cam_bone": { "fields": ["scale", "size"], "replace_with": 0 } } } 

📂 Подготовка файлов

Создайте CSV-файлы:

Оригинальные файлы: filename.csv

Модифицированные файлы: filename2.csv

Поместите файлы в директорию examples:

Nulls-brawl-csv2json-/ ├── examples/ │ ├── персонажи.csv # Оригинальный файл │ ├── персонажи2.csv # Модифицированный файл │ ├── способности.csv # Оригинальный файл │ └── способности2.csv # Модифицированный файл 

▶️ Запуск скрипта

python main.py 

📊 Результат

Сгенерированный файл мода будет сохранен как content.json в корне проекта.

📞 Support / Поддержка / Техническая поддержка

- Email: "yuq644691@gmail.com" (mailto:yuq644691@gmail.com)
- QQ: 3384853402
- GitHub Issues: "Report Problems" (https://github.com/QINGYU201004/Nulls-brawl-csv2json-/issues)

🔗 Repository Link

"https://github.com/QINGYU201004/Nulls-brawl-csv2json-" (https://github.com/QINGYU201004/Nulls-brawl-csv2json-)
