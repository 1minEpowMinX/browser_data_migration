> 🇬🇧 [Read in English](./README.md)

# 📦 Browser Data Migration

Утилита для **экспорта и импорта данных браузеров Chrome, Edge и Firefox** между компьютерами.  
Программа сохраняет текущие открытые вкладки и профили браузеров, включая настройки, расширения, историю и другие данные.

---

## 🚀 Возможности

- 📤 **Экспорт данных**:
  - текущие вкладки;
  - профили браузеров (настройки, расширения, кэш и т.д.).

- 📥 **Импорт данных**:
  - восстановление вкладок;
  - перенос пользовательских профилей.

- 📁 Поддержка популярных браузеров: **Chrome, Edge, Firefox**.

---

## 🖥️ Как использовать

### 📦 Экспорт данных
1. Запустите утилиту и выберите `1. Экспорт данных`.
2. Выберите целевой профиль на ПК.
3. Программа автоматически найдёт установленные браузеры и сохранит:
   - файл `browser_data.json`;
   - директории с профилями браузеров.

### 📥 Импорт данных
1. Перенесите файл `browser_data.json` и папки профилей на новый компьютер.
2. Запустите утилиту и выберите `2. Импорт данных`.
3. Утилита спросит о методе импорта. Выберите тот, который вам нужен.

---

## ⚠️ Важно
- При необходимости вы можете вручную отредактировать файл `browser_data.json`.
- **Не закрывайте браузер**, если хотите, чтобы вкладки автоматически **восстановились** — утилита сама завершит процесс.

---

## 🛠️ Установка

### 🖥️ Windows
1. Перейдите на вкладку [Releases](https://github.com/1minEpowMinX/browser_data_migration/releases).
2. Скачайте файл `browser-data-migration.exe`.
3. Запустите `.exe` — установка не требуется.

> ❗ При первом запуске Windows может предупредить о неизвестном издателе — это нормально для самосборных утилит.  

<br>

### 🐍 Установка из исходников (Windows & Linux)
1. Убедитесь, что у вас установлен **Python 3.9+**.
2. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/1minEpowMinX/browser-data-migration.git
   cd browser-data-migration
   ```
   
3. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

4. Запустите приложение:

   ```bash
   python main.py
   ```

---

## 📁 Структура проекта
```css
browser-data-migration/
├── assets/
│   ├── Project_icon_DALL.E.ico
├── migrations/
│   ├── exporter.py
│   ├── importer.py
├── session_parsers/
│   ├── chromium_parser.py
│   ├── firefox_parser.py
├── structrues/
│   ├── base_structures.py
│   ├── chormium_structures.py
│   ├── firefox_structures.py
├── ui/
│   ├── console.py
│   ├── menu.py
│   ├── messages.py
│   ├── status.py
├── utils/
│   ├── browser_paths.py
│   ├── check_browser_status.py
│   ├── json_handler.py
│   ├── logger.py
├── LICENSE
├── README.md
├── README.ru.md
├── main.py
├── requirements.txt
```

---

## 📄 License
MIT License — свободно используйте, модифицируйте и распространяйте.
