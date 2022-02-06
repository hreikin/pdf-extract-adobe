import logging, json, pytesseract, fitz

from pathlib import Path
from PIL import Image
from pdf2image import convert_from_path

def target_element_in_json(schema_source, target_element):
    """
    Recursively finds all JSON files within a given source directory before 
    individually extracting the JSON files content into a dictionary.
    
    The sub function "_iterate_through_nested_dicts()" is called on every 
    dictionary individually passing it a constructed filepath as the output file.

    :param schema_source: A directory containing JSON files.
    :param output_path: Location to create output files.
    """
    json_file_list = Path(schema_source).rglob("*.json")
    output_path = Path(schema_source).with_stem("extracted-content")
    for json_file in json_file_list:
        txt_output_dir = output_path / json_file.parent.name
        txt_output_dir.mkdir(parents=True, exist_ok=True)
        txt_output = txt_output_dir / json_file.name.replace(".json", ".txt")
        with json_file.open() as stream:
            extracted_json = json.loads(stream.read())
        logging.debug(f"Targeting '{target_element}' elements within '{json_file.resolve()}'.")
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

def split_all_pages_into_image(input_path, format):
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
    # To get better resolution
    zoom_x = 2.0
    zoom_y = 2.0
    zoom_matrix = fitz.Matrix(zoom_x, zoom_y)
    pdf_file_list = Path(input_path).rglob("*.pdf")
    for pdf_file in pdf_file_list:
        logging.debug(f"Converting '{pdf_file.resolve()}'.")
        doc = fitz.open(pdf_file)
        image_name = pdf_file.stem + "_page_"
        images_path = Path(input_path).with_stem("extracted-content") / pdf_file.stem
        Path(images_path).mkdir(parents=True, exist_ok=True)
        logging.debug(f"Image created at '{Path(image_name).resolve()}'.")
        for page in doc:
            pix = page.get_pixmap(matrix=zoom_matrix)
            pix.save(f"{images_path}/{image_name}{page.number}{format}")

def ocr_images_for_text(input_path, format):
    """
    Recursively finds all images of the given format and performs OCR on them to 
    create a text file containing the infomation that was found.

    :param input_path: Directory containing images.
    :param output_path: Directory to write the OCR content to.
    :param format: File type to use for the conversion without the leading dot
    """
    input_path = Path(input_path)
    for directory in input_path.iterdir():
        images_file_list = sorted(Path(directory).rglob(f"*{format}"))
        for item in images_file_list:
            split_name = item.name.split("_page_")
            txt_file_path = f"{input_path}/{split_name[0]}/{split_name[0]}-IMAGE-OCR.txt"
            logging.debug(f"Performing OCR on '{item.resolve()}'.")
            logging.debug(f"Creating text output file at '{Path(txt_file_path).resolve()}'.")
            ocr_string = pytesseract.image_to_string(Image.open(item))
            with open(txt_file_path, "a") as stream:
                stream.write(ocr_string)

def extract_text_from_pdf(input_path):
    input_path = Path(input_path)
    pdf_file_list = sorted(Path(input_path).rglob(f"*.pdf"))
    for pdf in pdf_file_list:
        txt_file_dir = f"{input_path.with_name('extracted-content')}/{pdf.stem}"
        txt_file_path = f"{txt_file_dir}/{pdf.stem}-PDF-EXTRACT.txt"
        Path(txt_file_dir).mkdir(parents=True, exist_ok=True)
        logging.debug(f"Extracting text from '{pdf.resolve()}'.")
        logging.debug(f"Creating text output file at '{Path(txt_file_path).resolve()}'.")
        with fitz.open(pdf) as doc:
            pdf_text = ""
            for page in doc:
                pdf_text += page.get_text()
        with open(txt_file_path, "a") as stream:
            stream.write(pdf_text)