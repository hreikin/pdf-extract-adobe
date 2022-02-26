import utilities.constants
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
                filename = directory.resolve() / "split-json" / f"{key}.json"
                filename.parent.mkdir(parents=True, exist_ok=True)
                with open(filename, 'w') as stream:
                    # Save each obj to their respective filepath
                    # with pretty formatting thanks to `indent=4`
                    json.dump(val, stream, indent=4)
            _split_elements_json(filename.parent.resolve())
            _sqlitebiter_import_json(filename.parent.resolve())

def _split_elements_json(src):
    src = Path(src).resolve()
    processing = list()
    elements_json = src / "elements.json"
    new_elements = elements_json.with_name(src.parent.name + ".json")
    with open(elements_json, "r")as stream:
        json_file = json.load(stream)
    _iterate_json(json_file, src, processing)
    final = []
    for dictionary in processing:
        temp_dict = dictionary
        split_path = str(dictionary["Element Type"]).lstrip("//").split("/")
        for item in split_path:
            if split_path[-1] in utilities.constants.figures:
                temp_dict["Element Type"] = split_path[-1]
                final.append(temp_dict)
                break
            if item in utilities.constants.headings:
                temp_dict["Element Type"] = item
                final.append(temp_dict)
                break
            if item in utilities.constants.lists:
                temp_dict["Element Type"] = item
                final.append(temp_dict)
                break
            if item in utilities.constants.paragraphs:
                temp_dict["Element Type"] = item
                final.append(temp_dict)
                break
            if item in utilities.constants.table_rows:
                temp_dict["Element Type"] = item
                final.append(temp_dict)
                break
    with open(new_elements, "w") as stream:
        json.dump(final, stream)

def _sqlitebiter_import_json(src):
    all_files = Path(src).rglob("*.json")
    db_out = Path(utilities.constants.database).resolve()
    db_out.parent.mkdir(parents=True, exist_ok=True)
    for file in all_files:
        if file.name == f"{Path(src).parent.name}.json":
            os.system(f"sqlitebiter -a -o {db_out} file {file}")

def _iterate_json(json_file,  src, processing):
    for sub_dict in json_file:
        keys_list = list(sub_dict.keys())
        values_list = list(sub_dict.values())
        for key, val in sub_dict.items():
            if key == "filePaths":
                filepath_index = keys_list.index(key)
                path_index = keys_list.index("Path")
                page_index = keys_list.index("Page")
                if len(values_list[filepath_index]) > 1:
                    temp_dict = {
                        "Text" : "N/A",
                        "Image Path" : f"{src.parent.resolve()}/{values_list[filepath_index][-1]}",
                        "Table Path" : f"{src.parent.resolve()}/{values_list[filepath_index][0]}",
                        "Path" : values_list[path_index],
                        "Element Type" : values_list[path_index],
                        "Page Num" : values_list[page_index],
                        }
                else:
                    temp_dict = {
                        "Text" : "N/A",
                        "Image Path" : f"{src.parent.resolve()}/{values_list[filepath_index][0]}",
                        "Table Path" : "N/A",
                        "Path" : values_list[path_index],
                        "Element Type" : values_list[path_index],
                        "Page Num" : values_list[page_index],
                        }
                processing.append(temp_dict)
            elif key == "Text":
                if sub_dict[key] in utilities.constants.unwanted_pdf[::]:
                    break
                text_index = keys_list.index(key)
                path_index = keys_list.index("Path")
                page_index = keys_list.index("Page")
                temp_dict = {
                    "Text" : values_list[text_index], 
                    "Image Path" : "N/A",
                    "Table Path" : "N/A",
                    "Path" : values_list[path_index],
                    "Element Type" : values_list[path_index],
                    "Page Num" : values_list[page_index],
                    }
                processing.append(temp_dict)
                txt_out = utilities.constants.confidence_dir / src.parent.name / f"{src.parent.name}-JSON-TXT.txt"
                txt_out.parent.mkdir(parents=True, exist_ok=True)
                with open(txt_out, "a") as stream:
                    stream.write(str(values_list[text_index]) + "\n")
            elif isinstance(val, list) and isinstance(val[0], dict):
                _iterate_json(val,  src, processing)

    return processing
# src = "../test/json-schema/"
# split_main_json_file(src)