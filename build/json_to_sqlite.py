import json
import os

from pathlib import Path

def split_main_json_file(src):
    src = Path(src).resolve()
    for directory in src.iterdir():
        json_files = directory.glob("structuredData.json")
        for file in json_files:
            with open(file, "r") as stream:
                full_dict = json.load(stream)
            for key, val in full_dict.items():
                filename = file.parent.resolve() / "split-json" / str(key + ".json")
                filename.parent.mkdir(parents=True, exist_ok=True)
                with open(filename, 'w') as stream:
                    # Save each obj to their respective filepath
                    # with pretty formatting thanks to `indent=4`
                    json.dump(val, stream, indent=4)
            _split_elements_json(filename.parent.resolve())
            _sqlitebiter_import_json(filename.parent.resolve())

def _split_elements_json(src):
    processing = list()
    elements = Path(src).resolve() / "elements.json"
    new_elements = elements.with_name(elements.parent.parent.name + ".json").resolve()
    headings = ["Title"]
    paragraphs = ["P", "LBody", "ParagraphSpan", "Span", "StyleSpan"]
    lists = ["L"]
    table_rows = ["TR"]
    figures = ["Figure", "Table"]
    for i in range(0, 101):
        headings.append(f"H{i}")
        paragraphs.append(f"P[{i}]")
        lists.append(f"LI[{i}]")
        table_rows.append(f"TR[{i}]")
        figures.append(f"Table[{i}]")
        figures.append(f"Figure[{i}]")
    with open(elements, "r")as stream:
        json_file = json.load(stream)
    for sub_dict in json_file:
        keys_list = list(sub_dict.keys())
        values_list = list(sub_dict.values())
        for key, val in sub_dict.items():
            if key == "filePaths":
                filepath_index = keys_list.index(key)
                path_index = keys_list.index("Path")
                page_index = keys_list.index("Page")
                temp_dict = {
                    "Text" : "null",
                    keys_list[filepath_index] : values_list[filepath_index][0],
                    keys_list[path_index] : values_list[path_index], 
                    keys_list[page_index] : values_list[page_index],
                    }
                processing.append(temp_dict)
            elif key == "Text":
                text_index = keys_list.index(key)
                path_index = keys_list.index("Path")
                page_index = keys_list.index("Page")
                temp_dict = {
                    keys_list[text_index] : values_list[text_index], 
                    "filePaths" : "null",
                    keys_list[path_index] : values_list[path_index], 
                    keys_list[page_index] : values_list[page_index],
                    }
                processing.append(temp_dict)
    final = []
    for dictionary in processing:
        temp_dict = dictionary
        split_path = str(dictionary["Path"]).lstrip("//").split("/")
        # print(split_path)
        for item in split_path:
            if split_path[-1] in figures:
                temp_dict["Path"] = split_path[-1]
                final.append(temp_dict)
                break
            if item in headings:
                temp_dict["Path"] = item
                final.append(temp_dict)
                break
            if item in lists:
                temp_dict["Path"] = item
                final.append(temp_dict)
                break
            if item in paragraphs:
                temp_dict["Path"] = item
                final.append(temp_dict)
                break
            if item in table_rows:
                temp_dict["Path"] = item
                final.append(temp_dict)
                break
    with open(new_elements, "w") as stream:
        json.dump(final, stream)

def _sqlitebiter_import_json(src):
    all_files = Path(src).rglob("*.json")
    db_out = Path(src).parent.parent.parent.resolve() / "sqlite" / "pcc.sqlite"
    db_out.parent.mkdir(parents=True, exist_ok=True)
    for file in all_files:
        if file.name == str(Path(src).parent.name + ".json"):
            os.system(f"sqlitebiter -a -o {db_out} file {file}")

# src = "../test/json-schema/"
# split_main_json_file(src)