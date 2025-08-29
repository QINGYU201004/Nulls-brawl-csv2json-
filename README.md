模组生成脚本使用指南 / Mod Generator Script User Guide / Руководство пользователя скрипта генерации модов

项目概述 / Project Overview / Обзор проекта

这是一个用于自动生成游戏模组的Python脚本工具，能够：

- 自动比较原版CSV文件和修改版CSV文件
- 提取差异并生成优化的JSON格式模组文件
- 支持批量处理多个CSV文件
- 提供数据验证和修复功能
- 生成详细的处理报告

This is a Python script tool for automatically generating game mods, capable of:

- Automatically comparing original CSV files and modified CSV files
- Extracting differences and generating optimized JSON format mod files
- Supporting batch processing of multiple CSV files
- Providing data validation and repair functions
- Generating detailed processing reports

Это инструмент на Python для автоматического создания модов для игр, который может:

- Автоматически сравнивать оригинальные CSV-файлы и модифицированные CSV-файлы
- Извлекать различия и генерировать оптимизированные файлы модов в формате JSON
- Поддерживать пакетную обработку нескольких CSV-файлов
- Предоставлять функции проверки и восстановления данных
- Генерировать подробные отчеты об обработке

快速开始 / Quick Start / Быстрый старт

安装依赖 / Install Dependencies / Установка зависимостей

pip install tqdm

或 / or / или

pip install -r requirements.txt

使用步骤 / Usage Steps / Шаги использования

1. 准备CSV文件：
   - 原版文件：
"filename.csv"
   - 修改版文件：
"filename2.csv"

Prepare CSV files:

- Original file: 
"filename.csv"
- Modified file: 
"filename2.csv"

Подготовьте CSV-файлы:

- Оригинальный файл: 
"filename.csv"
- Модифицированный файл: 
"filename2.csv"

2. 创建配置文件 
"config.json"（参考下方配置说明）

Create configuration file 
"config.json" (refer to configuration instructions below)

Создайте файл конфигурации 
"config.json" (см. инструкции по настройке ниже)

3. 运行脚本：

Run the script:

Запустите скрипт:

python main.py

4. 生成的模组文件将保存为 
"content.json"

The generated mod file will be saved as 
"content.json"

Сгенерированный файл мода будет сохранен как 
"content.json"

配置文件说明 (config.json) / Configuration File Description / Описание файла конфигурации

{
    "mod_metadata": {
        "title": "模组名称",
        "description": {
            "EN": "English description",
            "CN": "中文描述",
            "RU": "Описание на русском"
        },
        "author": "作者名称",
        "gv": 62
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

配置项说明 / Configuration Items Description / Описание элементов конфигурации

配置项 / Configuration Item / Элемент конфигурации 类型 / Type / Тип 说明 / Description / Описание 默认值 / Default Value / Значение по умолчанию

"mod_metadata" object 模组元数据 / Mod metadata / Метаданные мода -

"mod_metadata.title" string 模组标题 / Mod title / Название мода "综合修改模组" / "Comprehensive Mod" / "Комплексный мод"

"mod_metadata.description" object 多语言描述 / Multilingual description / Многоязычное описание {"CN": "自动生成的综合修改模组", "EN": "Automatically generated comprehensive mod", "RU": "Автоматически сгенерированный комплексный мод"}

"mod_metadata.author" string 作者信息 / Author information / Информация об авторе "自动生成" / "Auto Generated" / "Автоматически сгенерировано"

"mod_metadata.gv" integer 游戏版本 / Game version / Версия игры 1

"key_field" string 关键字段名 / Key field name / Имя ключевого поля "Name"

"data_folder" string 数据文件目录 / Data file directory / Директория файлов данных "." (当前目录 / current directory / текущая директория)

"csv_pattern" string 修改版文件匹配模式 / Modified file matching pattern / Шаблон соответствия модифицированных файлов "*2.csv"

"output_file" string 输出JSON文件名 / Output JSON filename / Имя выходного JSON-файла "content.json"

"numeric_fields" array 数字字段列表 / List of numeric fields / Список числовых полей []

"problem_values" object 问题值修复配置 / Problem value repair configuration / Конфигурация исправления проблемных значений {}

文件命名规则 / File Naming Rules / Правила именования файлов

文件类型 / File Type / Тип файла 命名规则 / Naming Rule / Правило именования 示例 / Example / Пример
原版文件 / Original file / Оригинальный файл 
"filename.csv" 
"skins.csv"
修改版文件 / Modified file / Модифицированный файл 
"filename2.csv" 
"skins2.csv"
配置文件 / Configuration file / Файл конфигурации 
"config.json" -
输出文件 / Output file / Выходной файл 由配置指定 / Specified by configuration / Указывается в конфигурации 
"content.json"

脚本功能 / Script Features / Функции скрипта

核心功能 / Core Features / Основные функции

1. 自动文件匹配 / Automatic File Matching / Автоматическое сопоставление файлов
   - 自动查找匹配的原版和修改版CSV文件对
   - 支持跳过不存在的文件
Automatically find matching original and modified CSV file pairs
   - Support skipping non-existent files
Автоматически находить соответствующие пары оригинальных и модифицированных CSV-файлов
   - Поддержка пропуска несуществующих файлов
2. 嵌套值提取 / Nested Value Extraction / Извлечение вложенных значений
   - 从CSV文件中提取嵌套数据结构
   - 支持进度条显示处理进度
Extract nested data structures from CSV files
   - Support progress bar display
Извлекать вложенные структуры данных из CSV-файлов
   - Поддержка отображения прогресс-бара
3. 差异比较 / Difference Comparison / Сравнение различий
   - 比较原版和修改版文件的差异
   - 识别新建和修改的字段
Compare differences between original and modified files
   - Identify new and modified fields
Сравнивать различия между оригинальными и модифицированными файлами
   - Определять новые и измененные поля
4. 数据验证 / Data Validation / Проверка данных
   - 验证数字字段的有效性
   - 自动修复常见问题值（如"cam_bone"）
Validate the validity of numeric fields
   - Automatically repair common problem values (e.g., "cam_bone")
Проверять корректность числовых полей
   - Автоматически исправлять распространенные проблемные значения (например, "cam_bone")
5. JSON生成 / JSON Generation / Генерация JSON
   - 生成优化的JSON格式模组文件
   - 支持多语言描述
Generate optimized JSON format mod files
   - Support multilingual descriptions
Генерировать оптимизированные файлы модов в формате JSON
   - Поддержка многоязычных описаний

高级功能 / Advanced Features / Расширенные функции

1. 性能优化 / Performance Optimization / Оптимизация производительности
   - 实时显示处理进度
   - 计算平均处理速度
   - 显示详细的时间统计
Real-time display of processing progress
   - Calculate average processing speed
   - Display detailed time statistics
Отображение прогресса обработки в реальном времени
   - Расчет средней скорости обработки
   - Отображение детальной статистики времени
2. 错误处理 / Error Handling / Обработка ошибок
   - 全面的异常捕获
   - 详细的错误信息
   - 自动跳过无效文件
Comprehensive exception capture
   - Detailed error information
   - Automatically skip invalid files
Комплексный перехват исключений
   - Подробная информация об ошибках
   - Автоматический пропуск недействительных файлов
3. 报告生成 / Report Generation / Генерация отчетов
   - 处理统计信息
   - 文件大小和行数报告
   - 修改数量统计
Processing statistics
   - File size and line count reports
   - Modification quantity statistics
Статистика обработки
   - Отчеты о размере файлов и количестве строк
   - Статистика количества изменений

注意事项 / Precautions / Меры предосторожности

1. 文件编码 / File Encoding / Кодировка файлов
   - 确保所有CSV文件使用UTF-8编码
   - 避免使用特殊字符作为字段名
Ensure all CSV files use UTF-8 encoding
   - Avoid using special characters as field names
Убедитесь, что все CSV-файлы используют кодировку UTF-8
   - Избегайте использования специальных символов в качестве имен полей
2. 数据格式 / Data Format / Формат данных
   - CSV文件必须包含标题行和类型行
   - 确保关键字段（如"Name"）存在且非空
CSV files must contain header rows and type rows
   - Ensure key fields (e.g., "Name") exist and are not empty
CSV-файлы должны содержать строки заголовков и типов
   - Убедитесь, что ключевые поля (например, "Name") существуют и не пусты
3. 性能考虑 / Performance Considerations / Соображения производительности
   - 大文件处理可能需要较长时间
   - 建议在性能较好的设备上运行
Processing large files may take a long time
   - Recommended to run on devices with good performance
Обработка больших файлов может занять много времени
   - Рекомендуется запускать на устройствах с хорошей производительностью
4. 问题值修复 / Problem Value Repair / Исправление проблемных значений
   - 在配置中定义需要修复的问题值
   - 确保修复后的值符合游戏要求
Define problem values that need repair in the configuration
   - Ensure repaired values meet game requirements
Определите проблемные значения, которые необходимо исправить, в конфигурации
   - Убедитесь, что исправленные значения соответствуют требованиям игры
5. 备份建议 / Backup Recommendations / Рекомендации по резервному копированию
   - 在处理前备份原始文件
   - 定期保存配置文件
Backup original files before processing
   - Regularly save configuration files
Создавайте резервные копии исходных файлов перед обработкой
   - Регулярно сохраняйте файлы конфигурации

示例目录结构 / Example Directory Structure / Пример структуры каталогов

模组生成/ / Mod Generation/ / Генерация модов/
├── config.json          # 配置文件 / Configuration file / Файл конфигурации
├── main.py              # 主脚本 / Main script / Главный скрипт
├── skins.csv            # 原版CSV文件 / Original CSV file / Оригинальный CSV-файл
├── skins2.csv           # 修改版CSV文件 / Modified CSV file / Модифицированный CSV-файл
├── animations.csv       # 原版动画文件 / Original animation file / Оригинальный файл анимаций
├── animations2.csv     # 修改版动画文件 / Modified animation file / Модифицированный файл анимаций
└── content.json         # 生成的模组文件 / Generated mod file / Сгенерированный файл мода

技术支持 / Technical Support / Техническая поддержка

如有任何问题或建议，请联系：

- 作者：清雨
- QQ：3384853402
- 邮箱："yuq644691@gmail.com" (mailto:yuq644691@gmail.com)

If you have any questions or suggestions, please contact:

- Author: Qingyu
- QQ: 3384853402
- Email: "yuq644691@gmail.com" (mailto:yuq644691@gmail.com)

Если у вас есть какие-либо вопросы или предложения, пожалуйста, свяжитесь:

- Автор: Qingyu
- QQ: 3384853402
- Email: "yuq644691@gmail.com" (mailto:yuq644691@gmail.com)

祝您使用愉快！ / Enjoy using! / Приятного использования!

附件下载 / Attachment Download / Загрузка вложений

完整的脚本文件已打包，请下载：

- "模组生成工具.zip" (无)

The complete script files have been packaged, please download:

- "Mod Generator Tool.zip" (无)

Полные файлы скрипта упакованы, пожалуйста, скачайте:

- "Инструмент генерации модов.zip" (无)

压缩包包含：

模组生成工具/ / Mod Generator Tool/ / Инструмент генерации модов/
├── config.json          # 配置文件 / Configuration file / Файл конфигурации
├── main.py              # 主脚本 / Main script / Главный скрипт
└── README.md            # 使用指南 / User Guide / Руководство пользователя