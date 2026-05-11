Folder Structure

KiCadQuickOpener/
├── Images/
│   ├── project.png   # Main search icon
│   ├── pcb.png       # Layout icon
│   ├── sch.png       # Schematic icon
│   └── folder.png    # Explorer icon
├── main.py           # The core logic
├── plugin.json       # Flow Launcher metadata
├── README.md         # Instructions and usage
└── doc.md            # app and code teardown

(Note: If you are missing the Images folder or the specific icon files, Flow Launcher will display a default fallback icon).
Usage

Trigger the plugin by typing `kc`  followed by your project name.

Enter: Opens the main KiCad project file.

`Shift + Enter` (or Right Arrow): Opens the context menu to select specific PCB/Schematic files or open the directory.


---

### 2. The `DOCS.md` File (Code Explanation)
Save this as `DOCS.md`. It breaks down the architecture and the JSON-RPC communication so you never forget how the internal gears turn.

markdown
# Code Architecture & Explanation

This plugin operates via **JSON-RPC**. Flow Launcher acts as the client, sending JSON requests to our Python script via the command line. The Python script processes the request and prints a JSON string back to the standard output, which Flow Launcher parses and displays.

## 1. The Entry Point (`__main__`)
Flow Launcher executes the script using the format: `python main.py <JSON_STRING>`. 
We catch this in the `__main__` block.

```python
if __name__ == "__main__":
    try:
        request = json.loads(sys.argv[1])
        method = request.get("method")
        parameters = request.get("parameters", [])
        # Route to query, context_menu, or open_file based on the method...
```

Why it's built this way: Flow Launcher 2.0+ passes everything as a single JSON string in the first system argument (sys.argv[1]). We parse it to figure out what action Flow Launcher wants us to take.

## 2. The query Function (Finding Projects)

When the user types kc blinker, Flow Launcher calls the query method.
Python
```python
def query(term):
    # ... directory checking logic ...
    for root, _, files in os.walk(SEARCH_DIR):
        for f in files:
            if f.endswith(".kicad_pro") and term in f.lower():
                results.append({
                    "Title": f.replace(".kicad_pro", ""),
                    "SubTitle": root,
                    "IcoPath": "Images/project.png",
                    "JsonRPCAction": {
                        "method": "open_file",
                        "parameters": [os.path.join(root, f)]
                    },
                    "ContextData": [root] 
                })
```
os.walk: Recursively scans the SEARCH_DIR to find any .kicad_pro files.

JsonRPCAction: Tells Flow Launcher what to do if the user presses Enter. Here, it triggers our open_file method with the full file path.

ContextData: The secret sauce for the `right-click` menu. We pass the folder's root path (root) to the context_menu function so it knows where to look for PCBs and Schematics.

## 3. The context_menu Function (Drill-down)

Triggered when the user presses `Shift + Enter`. Flow Launcher passes the ContextData from the query result back to this function.

```python
def context_menu(folder_path):
    # 1. Add an option to open the raw folder
    # ...
    # 2. Scan the folder for specific KiCad files
    files = os.listdir(folder_path)
    for f in sorted(files, reverse=True):
        if f.endswith(".kicad_pcb"):
            # Add PCB result
        elif f.endswith(".kicad_sch") or f.endswith(".sch"):
            # Add Schematic result
```
os.listdir: Unlike os.walk, this only looks at the immediate files inside the specific project folder, keeping the context menu fast and clean.

Filtering: It explicitly ignores -bak files and hidden files starting with . to keep the menu clutter-free.

## 4. The open_file Function (Execution)

This is the final step. Whether the user pressed Enter on the main project or a specific schematic, it routes here.

```python
def open_file(parameters):
    if len(parameters) > 0:
        os.startfile(parameters[0])
    print(json.dumps({"result": []}))
```
os.startfile: A built-in Windows command that acts exactly like double-clicking a file in Explorer. It hands the file off to the OS, which automatically opens KiCad.

Empty Result: Flow Launcher expects a JSON response even after an action is taken. Printing an empty result list ([]) tells Flow Launcher the action succeeded and it can close its window safely.