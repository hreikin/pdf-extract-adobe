import os, json, pytesseract

from PIL import Image
from pdf2image import convert_from_path
from difflib import SequenceMatcher

def extract_text_from_json(schema_source):
    """
    This function walks through a given directory finding all JSON files. Then 
    it extracts the JSON into a dictionary and creates an output text filepath.
    
    It then calls the sub function "_iterate_through_nested_dicts()" on every 
    dictionary individually passing it the text filepath as the output file.

    :param schema_source: A directory containing JSON files.
    """
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
    """
    Iterates through a dictionary targeting certain keys and values which are 
    written to an output file, it also checks if the values contain nested lists 
    or dictionaries, if they do it recursively calls this function on them.

    This sub function is called on the extracted JSON files which are found by 
    the function "extract_text_from_json()".

    :param nested_dict: A JSON dictionary.
    :param output_file: File to output targeted values to.
    """
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
    """
    Finds all PDF files within a directory and converts each page of each PDF to 
    an image using pdf2image. 
    
    The "convert_from_path()" parameter "thread_count" sets how many threads to 
    use for the conversion. The amount of threads used is never more than the 
    number of pages in a PDF.

    :param input_path: Directory containing PDF files.
    :param output_path: Directory to output the converted images to.
    :param format: Format of the converted image.
    """
    for root, dirnames, filenames in os.walk(input_path):
        for filename in filenames:
            image_name = filename.rstrip(".pdf") + "_page_"
            images_path = output_path + "/" + filename.rstrip(".pdf") + "/"
            if not os.path.isdir(images_path):
                os.makedirs(images_path, exist_ok=True)
            convert_from_path(root + "/" + filename, output_folder=images_path, output_file=image_name, thread_count=8, fmt=format)

def ocr_converted_pdf_images(input_path, output_path):
    """
    Find all the converted images from the function "convert_pdf_to_image()" and 
    process with pytesseract and Tesseract OCR to create a text file with the 
    found content.

    :param input_path: Directory containing directories of images created with the function "convert_pdf_to_image()".
    :param output_path: Text file to write the OCR content to.
    """
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
    """
    Walks through all directories in the given input path and finds two 
    pre-determined files to be used for a very basic confidence check.

    The confidence check uses the difflib sequence matcher to compares two files 
    created with the "_iterate_through_nested_dicts()" and 
    "ocr_converted_pdf_images()" functions before returning a score.

    The comparison is done both ways on the two files to create two different 
    scores which are then used to create an average confidence score for the 
    file. The scores for all files are added to a dictionary which is then 
    printed to the console to display the results.

    :param input_path: Directory containing other directories which contain the JSON Schema and extracted/OCR text files.
    """
    final_score_dict = {}
    with os.scandir(input_path) as dirs_list:
        for directory in dirs_list:
            for root, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    if filename == "structuredData.txt":
                        json_schema_txt = input_path + "/" + directory.name + "/" + filename
                    elif filename.endswith("-ocr.txt"):
                        ocr_txt = input_path + "/" + directory.name + "/" + filename
            ####################################################################
            # The Python docs state that "ratio()"" returns a float in [0, 1], 
            # measuring the similarity of the sequences. As a rule of thumb, a 
            # "ratio()"" value over 0.6 means the sequences are close matches:
            with open(json_schema_txt) as stream:
                txt_json = stream.read()
            with open(ocr_txt) as stream:
                txt_ocr = stream.read()
            score_a = SequenceMatcher(None, txt_json, txt_ocr)
            score_b = SequenceMatcher(None, txt_ocr, txt_json)
            average_score = (score_a.ratio() + score_b.ratio()) / 2
            final_score_dict[directory.name.replace('-Extracted-Json-Schema', '')] = {
                "Score A" : score_a.ratio(),
                "Score B" : score_b.ratio(),
                "Score Average" : average_score,
            }
    print("\nPDF FILE".ljust(50) + "SCORE".rjust(30))
    for pdf, scores in final_score_dict.items():
        print(f"{pdf}".ljust(50))
        for key, value in scores.items():
                print(f"{key}:".ljust(50) + f"{value}".rjust(30))
    output_file = "../test/confidence-score.txt"
    with open(output_file, "w") as stream:
        for pdf, scores in final_score_dict.items():
            stream.write(f"{pdf}:\n")
            for key, value in scores.items():
                stream.write(f"\t{key}:\t{value}\n")
            stream.write("")