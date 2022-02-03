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
                txt_file_dir = output_path + "/" + split_filenames[0] + "-Extracted-Json-Schema" + "/"
                txt_file_path = txt_file_dir + txt_file_name
                if not os.path.isdir(txt_file_dir):
                    os.makedirs(txt_file_dir, exist_ok=True)
                if not os.path.isdir(output_path):
                    os.makedirs(output_path, exist_ok=True)
                sorted_filenames_list = sorted(filenames)
                for filename in sorted_filenames_list:
                    image_file_path = root + "/" + filename
                    ocr_string = pytesseract.image_to_string(Image.open(image_file_path))
                    with open(txt_file_path, "a") as stream:
                        stream.write(ocr_string)

def confidence_check(input_path):
    final_score_dict = {}
    with os.scandir(input_path) as dirs_list:
        for directory in dirs_list:
            for root, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    if filename == "structuredData.txt":
                        json_schema_txt = input_path + "/" + directory.name + "/" + filename
                    elif filename.endswith("-ocr.txt"):
                        ocr_txt = input_path + "/" + directory.name + "/" + filename
            with open(json_schema_txt) as stream:
                txt_json = stream.read()
            with open(ocr_txt) as stream:
                txt_ocr = stream.read()
            score_a = SequenceMatcher(None, txt_json, txt_ocr)
            score_b = SequenceMatcher(None, txt_ocr, txt_json)
            final_score = (score_a.ratio() + score_b.ratio()) / 2
            final_score_dict[directory.name.replace('-Extracted-Json-Schema', '')] = {
                "Score A" : score_a.ratio(),
                "Score B" : score_b.ratio(),
                "Score Average" : final_score
            }
    for pdf, scores in final_score_dict.items():
        print(f"{pdf}:")
        for key, value in scores.items():
            print(f"\t{key}:\t{value}")
        print("")