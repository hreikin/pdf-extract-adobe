import os, json, pytesseract

from PIL import Image
from pdf2image import convert_from_path
from difflib import SequenceMatcher

def extract_text_from_json(schema_source):
    # Targets "Text" entries from the Json Schema and adds them to a file.
    for root, dirnames, filenames in os.walk(schema_source):
        for filename in filenames:
            if filename.endswith(".json"):
                file = os.path.join(root, filename)
                txt_file = os.path.join(root, filename.replace(".json", ".txt"))
                with open(file, "r") as stream:
                    extracted_json = json.loads(stream.read())
                _iterate_through_nested_dicts(extracted_json, txt_file)

def _iterate_through_nested_dicts(nested_dict, output_file):
    for key,value in nested_dict.items():
        if isinstance(value, dict):
            _iterate_through_nested_dicts(value, output_file)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    _iterate_through_nested_dicts(item, output_file)
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            _iterate_through_nested_dicts(item, output_file)
        else:
            if key == "Text":
                with open(output_file, "a") as stream:
                    stream.write(value + "\n")

def convert_pdf_to_image(input_path, output_path, format):
    for root, dirnames, filenames in os.walk(input_path):
        for filename in filenames:
            image_name = filename.rstrip(".pdf") + "_page_"
            images_path = output_path + "/" + filename.rstrip(".pdf") + "/"
            if not os.path.isdir(images_path):
                os.makedirs(images_path, exist_ok=True)
            convert_from_path(root + "/" + filename, output_folder=images_path, output_file=image_name, thread_count=8, fmt=format)

def ocr_converted_pdf_images(input_path, output_path):
    with os.scandir(input_path) as dirs_list:
        for directory in dirs_list:
            for root, dirnames, filenames in os.walk(directory):
                split_filenames = filenames[0].split("_page_")
                txt_file_name = split_filenames[0] + "-ocr.txt"
                txt_file_path = output_path + "/" + split_filenames[0] + "-Extracted-Json-Schema" + "/" + txt_file_name
                txt_file_dir = output_path + "/" + split_filenames[0] + "-Extracted-Json-Schema" + "/"
                if not os.path.isdir(txt_file_dir):
                    os.makedirs(txt_file_dir, exist_ok=True)
                if not os.path.isdir(output_path):
                    os.makedirs(output_path, exist_ok=True)
                sorted_filenames_list = sorted(filenames)
                for filename in sorted_filenames_list:
                    image_file_path = root + "/" + filename
                    with open(txt_file_path, "a") as stream:
                        stream.write(pytesseract.image_to_string(Image.open(image_file_path)))

def accuracy_check(json_schema_txt, ocr_txt):
    with open(json_schema_txt) as stream:
        txt_json = stream.read()
    with open(ocr_txt) as stream:
        txt_ocr = stream.read()
    score_a = SequenceMatcher(None, txt_json, txt_ocr)
    score_b = SequenceMatcher(None, txt_ocr, txt_json)
    print(f"Score A: {score_a.ratio()}")
    print(f"Score B: {score_b.ratio()}")