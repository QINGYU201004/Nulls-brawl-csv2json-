Null's Brawl CSV to JSON Mod Generator - 详细多语言使用指南

下面是完整的、支持多语言自由切换的详细使用指南，专为GitHub优化设计：

🌐 多语言导航

"English" (#english) | "中文" (#中文) | "Русский" (#русский)

<a name="english"></a>

🚀 English Guide (Full Instructions)

📥 Installation and Setup

1. Clone the repository:
git clone https://github.com/QINGYU201004/Nulls-brawl-csv2json-.git
cd Nulls-brawl-csv2json-
2. Install dependencies:
pip install -r requirements.txt
3. Configure your mod:Edit 
"config.json" with your preferred text editor:
{
  "mod_metadata": {
    "title": "Your Custom Mod",
    "description": {
      "EN": "English description for the mod",
      "CN": "中文描述（可选）",
      "RU": "Описание на русском (опционально)"
    },
    "author": "Your Name",
    "gv": 62
  },
  "key_field": "Name",
  "data_folder": "examples",
  "csv_pattern": "*2.csv",
  "output_file": "content.json",
  "numeric_fields": ["scale", "size", "value"],
  "problem_values": {
    "cam_bone": {
      "fields": ["scale", "size"],
      "replace_with": 0
    }
  }
}

📂 Preparing Your CSV Files

1. Create your mod files:
   - Original game files: 
"filename.csv"
   - Your modified files: 
"filename2.csv"
Example:
characters.csv     (original)
characters2.csv    (your modifications)
2. Place files in the correct directory:
   - Create an 
"examples" folder if it doesn't exist
   - Place your CSV files in the 
"examples" folder
Directory structure:
Nulls-brawl-csv2json-/
├── examples/
│   ├── characters.csv
│   ├── characters2.csv
│   ├── abilities.csv
│   └── abilities2.csv
├── config.json
├── main.py
└── ...

⚙️ Running the Generator

1. Execute the script:
python main.py
2. Understand the output:
开始生成模组: Your Custom Mod

处理: characters.csv -> characters2.csv
关键字段: Name
  开始提取CSV文件: characters.csv
    文件大小: 1.25 MB
    总行数: 1500
    提取进度: 100%|██████████| 1500/1500 [00:03<00:00, 482.34行/秒]
    提取完成: 120 个嵌套对象, 耗时: 3.12秒
  检测嵌套修改: 100%|██████████| 120/120 [00:00<00:00, 420.11对象/秒]
    比较完成: 发现 35 处修改 (5 项新建, 30 项修改), 耗时: 0.29秒
  处理完成: 找到 35 处修改, 耗时: 3.41秒

正在写入JSON文件: content.json
  写入JSON文件: 100%|██████████| 1/1 [00:00<00:00, 15.24文件/秒]

已生成模组文件: content.json
处理统计: 1 个文件对已处理, 0 个文件对被跳过
JSON写入耗时: 0.07秒
总处理时间: 3.58秒
平均处理速度: 0.35 MB/s

📦 Using the Generated Mod

1. Find the output file:
   - Generated mod: 
"content.json"
2. Integrate with Null's Brawl:
   - Place 
"content.json" in your game mods folder
   - Enable the mod in-game

🔧 Advanced Features

1. Batch processing multiple files:Simply add more CSV pairs to the 
"examples" folder:
examples/
├── characters.csv
├── characters2.csv
├── abilities.csv
├── abilities2.csv
├── weapons.csv
└── weapons2.csv
2. Custom problem value fixes:Add new rules to 
"problem_values" in config.json:
"invalid_value": {
  "fields": ["damage", "health"],
  "replace_with": 1
}
3. Add custom numeric fields:Extend the 
"numeric_fields" array:
"numeric_fields": [
  "scale", "size", "value", "damage", "health", "cooldown"
]

🛠️ GitHub Integration

1. Automate with GitHub Actions:Create 
".github/workflows/generate.yml":
name: Generate Mod
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Generate mod
      run: python main.py
    - name: Upload mod artifact
      uses: actions/upload-artifact@v3
      with:
        name: mod-file
        path: content.json
2. Version control your mods:
git add examples/ config.json
git commit -m "Add character balance changes"
git push origin main

<a name="中文"></a>

🚀 中文指南 (完整说明)

📥 安装与设置

1. 克隆仓库:
git clone https://github.com/QINGYU201004/Nulls-brawl-csv2json-.git
cd Nulls-brawl-csv2json-
2. 安装依赖:
pip install -r requirements.txt
3. 配置你的模组:用文本编辑器修改 
"config.json":
{
  "mod_metadata": {
    "title": "你的自定义模组",
    "description": {
      "EN": "English description (optional)",
      "CN": "中文模组描述",
      "RU": "Описание на русском (опционально)"
    },
    "author": "你的名字",
    "gv": 62
  },
  "key_field": "Name",
  "data_folder": "examples",
  "csv_pattern": "*2.csv",
  "output_file": "content.json",
  "numeric_fields": ["scale", "size", "value"],
  "problem_values": {
    "cam_bone": {
      "fields": ["scale", "size"],
      "replace_with": 0
    }
  }
}

📂 准备CSV文件

1. 创建模组文件:
   - 原版游戏文件: 
"filename.csv"
   - 你的修改文件: 
"filename2.csv"
示例:
角色.csv     (原版)
角色2.csv    (你的修改)
2. 将文件放入正确目录:
   - 如果不存在，创建 
"examples" 文件夹
   - 将CSV文件放入 
"examples" 文件夹
目录结构:
Nulls-brawl-csv2json-/
├── examples/
│   ├── 角色.csv
│   ├── 角色2.csv
│   ├── 技能.csv
│   └── 技能2.csv
├── config.json
├── main.py
└── ...

⚙️ 运行生成器

1. 执行脚本:
python main.py
2. 理解输出信息:
开始生成模组: 你的自定义模组

处理: 角色.csv -> 角色2.csv
关键字段: Name
  开始提取CSV文件: 角色.csv
    文件大小: 1.25 MB
    总行数: 1500
    提取进度: 100%|██████████| 1500/1500 [00:03<00:00, 482.34行/秒]
    提取完成: 120 个嵌套对象, 耗时: 3.12秒
  检测嵌套修改: 100%|██████████| 120/120 [00:00<00:00, 420.11对象/秒]
    比较完成: 发现 35 处修改 (5 项新建, 30 项修改), 耗时: 0.29秒
  处理完成: 找到 35 处修改, 耗时: 3.41秒

正在写入JSON文件: content.json
  写入JSON文件: 100%|██████████| 1/1 [00:00<00:00, 15.24文件/秒]

已生成模组文件: content.json
处理统计: 1 个文件对已处理, 0 个文件对被跳过
JSON写入耗时: 0.07秒
总处理时间: 3.58秒
平均处理速度: 0.35 MB/s

📦 使用生成的模组

1. 找到输出文件:
   - 生成的模组: 
"content.json"
2. 整合到Null's Brawl:
   - 将 
"content.json" 放入游戏的模组文件夹
   - 在游戏中启用模组

🔧 高级功能

1. 批量处理多个文件:只需在 
"examples" 文件夹中添加更多CSV对:
examples/
├── 角色.csv
├── 角色2.csv
├── 技能.csv
├── 技能2.csv
├── 武器.csv
└── 武器2.csv
2. 自定义问题值修复:在config.json中添加新的 
"problem_values" 规则:
"invalid_value": {
  "fields": ["damage", "health"],
  "replace_with": 1
}
3. 添加自定义数字字段:扩展 
"numeric_fields" 数组:
"numeric_fields": [
  "scale", "size", "value", "damage", "health", "cooldown"
]

🛠️ GitHub集成

1. 使用GitHub Actions自动化:创建 
".github/workflows/generate.yml":
name: 生成模组
on: [push]
jobs:
  构建:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: 设置Python环境
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    - name: 安装依赖
      run: pip install -r requirements.txt
    - name: 生成模组
      run: python main.py
    - name: 上传模组
      uses: actions/upload-artifact@v3
      with:
        name: 模组文件
        path: content.json
2. 版本控制你的模组:
git add examples/ config.json
git commit -m "添加角色平衡修改"
git push origin main

<a name="русский"></a>

🚀 Русское руководство (Полные инструкции)

📥 Установка и настройка

1. Клонируйте репозиторий:
git clone https://github.com/QINGYU201004/Nulls-brawl-csv2json-.git
cd Nulls-brawl-csv2json-
2. Установите зависимости:
pip install -r requirements.txt
3. Настройте ваш мод:Отредактируйте 
"config.json" в текстовом редакторе:
{
  "mod_metadata": {
    "title": "Ваш кастомный мод",
    "description": {
      "EN": "English description (optional)",
      "CN": "中文描述 (可选)",
      "RU": "Описание мода на русском"
    },
    "author": "Ваше имя",
    "gv": 62
  },
  "key_field": "Name",
  "data_folder": "examples",
  "csv_pattern": "*2.csv",
  "output_file": "content.json",
  "numeric_fields": ["scale", "size", "value"],
  "problem_values": {
    "cam_bone": {
      "fields": ["scale", "size"],
      "replace_with": 0
    }
  }
}

📂 Подготовка CSV-файлов

1. Создайте файлы мода:
   - Оригинальные файлы игры: 
"filename.csv"
   - Ваши модифицированные файлы: 
"filename2.csv"
Пример:
персонажи.csv     (оригинал)
персонажи2.csv    (ваши модификации)
2. Разместите файлы в правильной директории:
   - Создайте папку 
"examples", если её нет
   - Поместите CSV-файлы в папку 
"examples"
Структура директории:
Nulls-brawl-csv2json-/
├── examples/
│   ├── персонажи.csv
│   ├── персонажи2.csv
│   ├── способности.csv
│   └── способности2.csv
├── config.json
├── main.py
└── ...

⚙️ Запуск генератора

1. Выполните скрипт:
python main.py
2. Понимание вывода:
Начало генерации мода: Ваш кастомный мод

Обработка: персонажи.csv -> персонажи2.csv
Ключевое поле: Name
  Начало извлечения CSV-файла: персонажи.csv
    Размер файла: 1.25 MB
    Всего строк: 1500
    Прогресс извлечения: 100%|██████████| 1500/1500 [00:03<00:00, 482.34 строк/сек]
    Извлечение завершено: 120 вложенных объектов, затрачено времени: 3.12сек
  Обнаружение вложенных изменений: 100%|██████████| 120/120 [00:00<00:00, 420.11 объектов/сек]
    Сравнение завершено: найдено 35 изменений (5 новых, 30 измененных), затрачено времени: 0.29сек
  Обработка завершена: найдено 35 изменений, затрачено времени: 3.41сек

Запись JSON-файла: content.json
  Запись JSON-файла: 100%|██████████| 1/1 [00:00<00:00, 15.24 файлов/сек]

Сгенерирован файл мода: content.json
Статистика обработки: обработано 1 пар файлов, пропущено 0 пар файлов
Время записи JSON: 0.07сек
Общее время обработки: 3.58сек
Средняя скорость обработки: 0.35 MB/сек

📦 Использование сгенерированного мода

1. Найдите выходной файл:
   - Сгенерированный мод: 
"content.json"
2. Интеграция с Null's Brawl:
   - Поместите 
"content.json" в папку модов игры
   - Включите мод в игре

🔧 Расширенные функции

1. Пакетная обработка нескольких файлов:Просто добавьте больше CSV-пар в папку 
"examples":
examples/
├── персонажи.csv
├── персонажи2.csv
├── способности.csv
├── способности2.csv
├── оружия.csv
└── оружия2.csv
2. Настройка исправления проблемных значений:Добавьте новые правила в 
"problem_values" в config.json:
"invalid_value": {
  "fields": ["damage", "health"],
  "replace_with": 1
}
3. Добавление пользовательских числовых полей:Расширьте массив 
"numeric_fields":
"numeric_fields": [
  "scale", "size", "value", "damage", "health", "cooldown"
]

🛠️ Интеграция с GitHub

1. Автоматизация с GitHub Actions:Создайте 
".github/workflows/generate.yml":
name: Генерация мода
on: [push]
jobs:
  сборка:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Настройка Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    - name: Установка зависимостей
      run: pip install -r requirements.txt
    - name: Генерация мода
      run: python main.py
    - name: Загрузка артефакта мода
      uses: actions/upload-artifact@v3
      with:
        name: файл-мода
        path: content.json
2. Контроль версий ваших модов:
git add examples/ config.json
git commit -m "Добавлены изменения баланса персонажей"
git push origin main

📞 Support / Поддержка / Техническая поддержка

- Email: "yuq644691@gmail.com" (mailto:yuq644691@gmail.com)
- QQ: 3384853402
- GitHub Issues: "Report Problems" (https://github.com/QINGYU201004/Nulls-brawl-csv2json-/issues)

🔗 Repository Link

"https://github.com/QINGYU201004/Nulls-brawl-csv2json-" (https://github.com/QINGYU201004/Nulls-brawl-csv2json-)
