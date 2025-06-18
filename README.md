> 🇷🇺 [Читать на Русском](./README.ru.md)


# 📦 Browser Data Migration

A utility for **exporting and importing data from Chrome, Edge, and Firefox browsers** between computers.  
The tool saves currently open tabs and browser profiles, including settings, extensions, history, and more.

---

## 🚀 Features

- 📤 **Export data**:
  - currently open tabs;
  - full browser profiles (settings, extensions, cache, etc.).

- 📥 **Import data**:
  - restore tabs;
  - transfer browser profiles.

- 📁 Supports popular browsers: **Chrome, Edge, Firefox**.

---

## 🖥️ How to Use

### 📦 Export Data
1. Run the utility and select `1. Export Data`.
2. Choose target profile from PC.
3. The program will detect installed browsers and save:
   - a `browser_data.json` file;
   - directories with browser profiles.

### 📥 Import Data
1. Transfer `browser_data.json` and profile folders to the new computer.
2. Run the utility and select `2. Import Data`.
3. The utility will ask about the import method. Select the one what you need.

---

## ⚠️ Important Notes
- You can manually edit the `browser_data.json` file if needed.
- **Keep the browser open** if you want tabs to auto-**restore** — the utility will close it automatically at the right time.

---

## 🛠️ Installation

### 🖥️ Windows

1. Go to the [Releases](https://github.com/1minEpowMinX/browser_data_migration/releases) tab.
2. Download the `browser-data-migration.exe` file.
3. Run the `.exe` — no installation required.

> ❗ On first launch, Windows may warn about an unknown publisher — this is normal for self-built utilities.

<br>

### 🐍 Install from source (Windows & Linux)

1. Make sure **Python 3.9+** is installed.
2. Clone the repository:

   ```bash
   git clone https://github.com/1minEpowMinX/browser-data-migration.git
   cd browser-data-migration
   ```
   
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:

   ```bash
   python main.py
   ```

---

## 📁 Project Structure

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
MIT License — feel free to use, modify, and distribute this project.
