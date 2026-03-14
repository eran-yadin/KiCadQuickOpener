# KiCad Quick Opener for Flow Launcher

A lightweight, zero-dependency Python plugin for [Flow Launcher](https://www.flowlauncher.com/) that lets you instantly search and open KiCad projects, PCBs, and Schematics directly from your keyboard.

## Features
* **Lightning Fast:** Uses built-in Python libraries; no external dependencies or SDKs required.
* **Smart Search:** Type a keyword to instantly find `.kicad_pro` files across your project directories.
* **Context Menu Drill-down:** Press `Shift + Enter` on a project to reveal specific layouts (`.kicad_pcb`), schematics (`.kicad_sch` / `.sch`), or just open the project folder in Windows Explorer.

## Installation

1. Open Flow Launcher and type `open settings folder`.
2. Navigate to the `Plugins` directory.
3. Clone or download this repository into a new folder named `KiCadQuickOpener`.
4. **Configuration:** Open `main.py` in a text editor and change the `SEARCH_DIR` variable on line 6 to point to your actual KiCad projects folder.
   ```python
   SEARCH_DIR = r"C:\path\to\your\projects"