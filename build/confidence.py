import json, pytesseract, logging

from pathlib import Path
from PIL import Image
from pdf2image import convert_from_path
from difflib import SequenceMatcher, get_close_matches

def target_element_in_json(schema_source, output_path, target_element):
    """
    Recursively finds all JSON files within a given source directory before 
    individually extracting the JSON files content into a dictionary.
    
    The sub function "_iterate_through_nested_dicts()" is called on every 
    dictionary individually passing it a constructed filepath as the output file.

    :param schema_source: A directory containing JSON files.
    :param output_path: Location to create output files.
    """
    # Targets "Text" entries from the Json Schema and adds them to a file.
    json_file_list = Path(schema_source).rglob("*.json")
    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)
    for json_file in json_file_list:
        txt_output_dir = output_path / json_file.parent.name
        txt_output_dir.mkdir(parents=True, exist_ok=True)
        txt_output = txt_output_dir / json_file.name.replace(".json", ".txt")
        with json_file.open() as stream:
            extracted_json = json.loads(stream.read())
        logging.debug(f"Targeting 'Text' elements within '{json_file.resolve()}'.")
        logging.debug(f"Creating text output file at '{txt_output.resolve()}'.")
        _iterate_through_nested_dicts(extracted_json, txt_output, target_element)

def _iterate_through_nested_dicts(nested_dict, output_file, target_element):
    """
    Recursively iterates through a dictionary and targets all "Text" keys and 
    their values to write to an output file.

    This sub function is called on the JSON files which are found by the function 
    "extract_text_from_json()".

    :param nested_dict: A JSON dictionary.
    :param output_file: File to output targeted values to.
    """
    for key,value in nested_dict.items():
        if isinstance(value, dict):
            _iterate_through_nested_dicts(value, output_file, target_element)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    _iterate_through_nested_dicts(item, output_file, target_element)
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            _iterate_through_nested_dicts(item, output_file, target_element)
        else:
            if key == target_element:
                logging.debug(f"Found '{key}' element: '{value}'")
                with open(output_file, "a") as stream:
                    stream.write(value + "\n")

def split_all_pages_image(input_path, output_path, format):
    """
    Recursively finds all PDF files within a given directory and converts each 
    page of each PDF to an image using pdf2image. 
    
    The "convert_from_path()" parameter "thread_count" sets how many threads to 
    use for the conversion. The amount of threads used is never more than the 
    number of pages in a PDF.

    :param input_path: Directory containing PDF files.
    :param output_path: Directory to output the converted images to.
    :param format: File type to use for the conversion without the leading dot.
    """
    pdf_file_list = Path(input_path).rglob("*.pdf")
    for pdf_file in pdf_file_list:
        image_name = pdf_file.stem + "_page_"
        images_path = output_path + pdf_file.stem
        Path(images_path).mkdir(parents=True, exist_ok=True)
        logging.debug(f"Converting '{pdf_file.resolve()}'.")
        logging.debug(f"Image created at '{Path(image_name).resolve()}'.")
        convert_from_path(pdf_file, output_folder=images_path, output_file=image_name, thread_count=8, fmt=format)

def ocr_images(input_path, output_path, format):
    """
    Recursively finds all images of the given format and performs OCR on them to 
    create a text file containing the infomation that was found.

    :param input_path: Directory containing images.
    :param output_path: Directory to write the OCR content to.
    :param format: File type to use for the conversion without the leading dot
    """
    input_path = Path(input_path)
    output_path = Path(output_path)
    for directory in input_path.iterdir():
        images_file_list = sorted(Path(directory).rglob(f"*.{format}"))
        for item in images_file_list:
            split_name = item.name.split("_page_")
            txt_file_path = f"{output_path}/{split_name[0]}-Extracted-Json-Schema/{split_name[0]}-OCR.txt"
            logging.debug(f"Performing OCR on '{item.resolve()}'.")
            logging.debug(f"Creating text output file at '{Path(txt_file_path).resolve()}'.")
            ocr_string = pytesseract.image_to_string(Image.open(item))
            with open(txt_file_path, "a") as stream:
                stream.write(ocr_string)

def confidence_check_text(input_path):
    """
    Recursively finds two pre-determined text files to be used for a very basic 
    confidence check.

    The confidence check uses the difflib "SequenceMatcher" class and 
    "get_close_matches()" method to compare two files created with the 
    "_iterate_through_nested_dicts()" and "ocr_converted_pdf_images()" functions 
    before returning a ratio. All ratios and averages are stored to a dictionary 
    and text file.

    The Python docs state that "ratio()" returns a float in [0, 1], measuring 
    the similarity of the sequences. As a rule of thumb, a "ratio()" value over 
    0.6 means the sequences are close matches. The same value of 0.6 is used as 
    the cut-off for the "get_close_matches()" method.

    :param input_path: Directory which contains the extracted/OCR text files.
    """
    input_path = Path(input_path)
    final_score_dict = dict()
    for directory in input_path.iterdir():
        if directory.is_dir() and directory.name.endswith("-Extracted-Json-Schema"):
            txt_file_list = sorted(directory.rglob("*.txt"))
            ocr_txt_file = txt_file_list[0]
            json_txt_file = txt_file_list[-1]
            logging.debug(f"Comparing '{ocr_txt_file.resolve()}' with '{json_txt_file.resolve()}'")
            with open(ocr_txt_file) as stream:
                ocr_list = stream.readlines()
            with open(json_txt_file) as stream:
                json_list = stream.readlines()
            close_matches_a = 0
            for line in ocr_list:
                matches_list = get_close_matches(line, json_list, n=1)
                if len(matches_list) > 0:
                    close_matches_a += 1
                matches_list = []
            close_match_ratio_a = close_matches_a / len(ocr_list)
            close_matches_b = 0
            for line in json_list:
                matches_list = get_close_matches(line, ocr_list, n=1)
                if len(matches_list) > 0:
                    close_matches_b += 1
                matches_list = []
            close_match_ratio_b = close_matches_b / len(json_list)
            with open(ocr_txt_file) as stream:
                ocr_string = stream.read()
            with open(json_txt_file) as stream:
                json_string = stream.read()
            reverse_ocr_string = ocr_string[::-1]
            reverse_json_string = json_string[::-1]
            score_a = SequenceMatcher(None, json_string, ocr_string)
            score_b = SequenceMatcher(None, ocr_string, json_string)
            score_c = SequenceMatcher(None, reverse_json_string, reverse_ocr_string)
            score_d = SequenceMatcher(None, reverse_ocr_string, reverse_json_string)
            comparison_ratio = (score_a.ratio() + score_b.ratio() + score_c.ratio() + score_d.ratio()) / 4
            close_match_average_ratio = (close_match_ratio_a + close_match_ratio_b) / 2
            total_average_ratio = (comparison_ratio + close_match_average_ratio) / 2
            logging.debug(f"Close Match Ratio A: '{close_match_ratio_a}'")
            logging.debug(f"Close Match Ratio B: '{close_match_ratio_b}'")
            logging.debug(f"Close Match Average Ratio: '{close_match_average_ratio}'")
            logging.debug(f"Comparison Ratio: '{comparison_ratio}'")
            logging.debug(f"Total Average Ratio: '{total_average_ratio}'")
            final_score_dict[directory.name.replace('-Extracted-Json-Schema', '')] = {
                "Comparison A Ratio" : score_a.ratio(),
                "Comparison B Ratio" : score_b.ratio(),
                "Comparison C Ratio" : score_c.ratio(),
                "Comparison D Ratio" : score_d.ratio(),
                "Comparison Average Ratio" : comparison_ratio,
                "Close Match Ratio A" : close_match_ratio_a,
                "Close Match Ratio B" : close_match_ratio_b,
                "Close Match Average Ratio" : close_match_average_ratio,
                "Total Average Ratio" : total_average_ratio,
            }
    output_file = "../test/confidence-check/all-confidence-scores.txt"
    logging.debug(f"Creating text output file with results '{Path(output_file).resolve()}'.")
    with open(output_file, "w") as stream:
        stream.write(f"PDF".ljust(50) + f"Score".rjust(30))
        for pdf, scores in final_score_dict.items():
            stream.write(f"\n{pdf}\n")
            for key, value in scores.items():
                stream.write(f"---- {key}:".ljust(50) + f"{round(value, 1)}\n".rjust(30))
