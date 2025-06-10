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
2. The program will detect installed browsers and save:
   - a `browser_data.json` file;
   - directories with browser profiles.

### 📥 Import Data
1. Transfer `browser_data.json` and profile folders to the new computer.
2. Run the utility and select `2. Import Data`.

---

## ⚠️ Important Notes

- Make sure to transfer data **between matching user profiles** (e.g., same user name).
- You can manually edit the `browser_data.json` file if needed — specifically the  
  `["browsers"][<browser_name>]["export_path"]` value.
- **Keep the browser open** if you want tabs to auto-**restore** — the utility will close it automatically at the right time.

---

## 🛠️ Installation

1. Make sure Python 3.9+ is installed.
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
│   ├── status.py
├── utils/
│   ├── browser_paths.py
│   ├── check_browser_status.py
│   ├── json_handler.py
│   ├── logger.py
├── LICENSE
├── main.py
├── README.md
├── requirements.txt
```

---

## 📄 License
MIT License — feel free to use, modify, and distribute this project.
