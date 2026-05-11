import sys
import json
import os

# Update this to your exact projects folder
SEARCH_DIR = r"C:\projects"

def query(term):
    results = []
    term = term.lower()
    
    if not os.path.exists(SEARCH_DIR):
        return [{"Title": "Error", "SubTitle": f"Path not found: {SEARCH_DIR}", "IcoPath": ""}]

    for root, _, files in os.walk(SEARCH_DIR):
        for f in files:
            if f.endswith(".kicad_pro") and term in f.lower():
                results.append({
                    "Title": f.replace(".kicad_pro", ""),
                    "SubTitle": root,
                    "IcoPath": "icons/icon.png", # Icon for the main project
                    "JsonRPCAction": {
                        "method": "open_file",
                        "parameters": [os.path.join(root, f)]
                    },
                    # This passes the folder path to the context_menu method
                    "ContextData": [root] 
                })
    return results

def context_menu(folder_path):
    results = []
    
    # 1. Option to open the project folder in Windows Explorer
    results.append({
        "Title": "Open Project Folder",
        "SubTitle": folder_path,
        "IcoPath": "icons/folder.png", # Icon for the folder
        "JsonRPCAction": {
            "method": "open_file",
            "parameters": [folder_path] # os.startfile opens directories natively
        }
    })
    
    # 2. Find PCBs and Schematics inside that folder
    try:
        files = os.listdir(folder_path)
        # Sort so PCBs appear first
        for f in sorted(files, reverse=True):
            if "-bak" in f or f.startswith("."):
                continue # Skip backup files
                
            full_path = os.path.join(folder_path, f)
            if f.endswith(".kicad_pcb"):
                results.append({
                    "Title": f"PCB: {f}",
                    "SubTitle": "Open Layout",
                    "IcoPath": "icons/pcb.png", # Icon for PCB
                    "JsonRPCAction": {"method": "open_file", "parameters": [full_path]}
                })
            elif f.endswith(".kicad_sch") or f.endswith(".sch"):
                results.append({
                    "Title": f"Schematic: {f}",
                    "SubTitle": "Open Schematic",
                    "IcoPath": "icons/sch.png", # Icon for Schematic
                    "JsonRPCAction": {"method": "open_file", "parameters": [full_path]}
                })
    except Exception as e:
        results.append({"Title": "Error", "SubTitle": str(e), "IcoPath": ""})
        
    return results

if __name__ == "__main__":
    try:
        request = json.loads(sys.argv[1])
        method = request.get("method")
        parameters = request.get("parameters", [])

        if method == "query":
            term = parameters[0] if len(parameters) > 0 else ""
            print(json.dumps({"result": query(term)}))
            
        elif method == "context_menu":
            # Extract the folder path passed from ContextData
            folder_path = parameters[0][0] if len(parameters) > 0 and len(parameters[0]) > 0 else ""
            print(json.dumps({"result": context_menu(folder_path)}))
            
        elif method == "open_file":
            if len(parameters) > 0:
                os.startfile(parameters[0])
            print(json.dumps({"result": []}))
            
    except Exception as e:
        print(json.dumps({"result": [{"Title": "Script Error", "SubTitle": str(e), "IcoPath": ""}]}))