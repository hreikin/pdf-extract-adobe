import json, pytesseract, fitz, os

from pathlib import Path
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
    json_file_list = Path(schema_source).rglob("*.json")
    for json_file in json_file_list:
        txt_output = json_file.with_suffix(".txt")
        with json_file.open() as stream:
            extracted_json = json.loads(stream.read())
        _iterate_through_nested_dicts(extracted_json, txt_output)

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
    pdf_file_list = Path(input_path).rglob("*.pdf")
    for pdf_file in pdf_file_list:
        image_name = pdf_file.stem + "_page_"
        images_path = output_path + pdf_file.stem
        Path(images_path).mkdir(parents=True, exist_ok=True)
        convert_from_path(pdf_file, output_folder=images_path, output_file=image_name, thread_count=8, fmt=format)

def ocr_converted_pdf_images(input_path, output_path, format):
    """
    Find all the converted images from the function "convert_pdf_to_image()" and 
    process with pytesseract and Tesseract OCR to create a text file with the 
    found content.

    :param input_path: Directory containing directories of images created with the function "convert_pdf_to_image()".
    :param output_path: Text file to write the OCR content to.
    """
    input_path = Path(input_path)
    output_path = Path(output_path)
    for directory in input_path.iterdir():
        images_file_list = sorted(Path(directory).rglob(f"*.{format}"))
        for item in images_file_list:
            split_name = item.name.split("_page_")
            txt_file_path = f"{output_path}/{split_name[0]}-Extracted-Json-Schema/{split_name[0]}-OCR.txt"
            ocr_string = pytesseract.image_to_string(Image.open(item))
            with open(txt_file_path, "a") as stream:
                stream.write(ocr_string)

def confidence_check_text(input_path):
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
    input_path = Path(input_path)
    final_score_dict = dict()
    for directory in input_path.iterdir():
        if directory.is_dir():
            txt_file_list = sorted(directory.rglob("*.txt"))
            ocr_txt_file = txt_file_list[0]
            json_txt_file = txt_file_list[-1]
            with open(ocr_txt_file) as stream:
                ocr_string = stream.read()
            with open(json_txt_file) as stream:
                json_string = stream.read()
            reverse_ocr_string = ocr_string[::-1]
            reverse_json_string = json_string[::-1]
            ####################################################################
            # The Python docs state that "ratio()"" returns a float in [0, 1], 
            # measuring the similarity of the sequences. As a rule of thumb, a 
            # "ratio()"" value over 0.6 means the sequences are close matches.
            score_a = SequenceMatcher(None, json_string, ocr_string)
            score_b = SequenceMatcher(None, ocr_string, json_string)
            score_c = SequenceMatcher(None, reverse_json_string, reverse_ocr_string)
            score_d = SequenceMatcher(None, reverse_ocr_string, reverse_json_string)
            average_score = (score_a.ratio() + score_b.ratio() + score_c.ratio() + score_d.ratio()) / 4
            final_score_dict[directory.name.replace('-Extracted-Json-Schema', '')] = {
                "Score A" : score_a.ratio(),
                "Score B" : score_b.ratio(),
                "Score C" : score_c.ratio(),
                "Score D" : score_d.ratio(),
                "Score Average" : average_score,
            }
    print("\nPDF FILE".ljust(50) + "SCORE".rjust(30))
    for pdf, scores in final_score_dict.items():
        print(f"{pdf}".ljust(50))
        for key, value in scores.items():
                print(f"{key}:".ljust(50) + f"{round(value, 2)}".rjust(30))
    output_file = "../test/confidence-score.txt"
    with open(output_file, "w") as stream:
        stream.write(f"PDF".ljust(50) + f"Score\n".rjust(30))
        for pdf, scores in final_score_dict.items():
            stream.write("\n")
            stream.write(f"{pdf}\n")
            for key, value in scores.items():
                stream.write(f"{key}:".ljust(50) + f"\t{round(value, 2)}\n".rjust(30))



# def extract_images_from_pdf(input_path, output_path):
#     for root, dirnames, filenames in os.walk(input_path):
#         for filename in filenames:
#             doc = fitz.open(f"{input_path}/{filename}")
#             dir_name = filename.rstrip(".pdf")
#             dir_path = output_path + "/" + dir_name
#             if not os.path.isdir(dir_path):
#                 os.makedirs(dir_path, exist_ok=True)
#             for i in range(len(doc)):
#                 for img in doc.get_page_images(i):
#                     xref = img[0]
#                     pix = fitz.Pixmap(doc, xref)
#                     if pix.n - pix.alpha < 4:       # this is GRAY or RGB
#                         pix.save(f"{dir_path}/p{i}-{xref}.png")
#                     else:               # CMYK: convert to RGB first
#                         pix1 = fitz.Pixmap(fitz.csRGB, pix)
#                         pix1.save(f"{dir_path}/p{i}-{xref}.png")
#                         pix1 = None
#                     pix = None
#
# def extract_images_from_pdf(input_path, output_path):
#     for root, dirnames, filenames in os.walk(input_path):
#         for filename in filenames:
#             dir_name = filename.rstrip(".pdf")
#             dir_path = output_path + "/" + dir_name
#             image_name = "extracted-image"
#             if not os.path.isdir(dir_path):
#                 os.makedirs(dir_path, exist_ok=True)
#             os.system(f"pdfimages -png {input_path}/{filename} {dir_path}/{image_name}")