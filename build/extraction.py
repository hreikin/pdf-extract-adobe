import parse_tab
import logging, json, pytesseract, fitz
import pandas as pd

from pathlib import Path
from PIL import Image

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
        txt_output = txt_output_dir / str(txt_output_dir.name + "-EXTRACTED-JSON.txt")
        md_output = txt_output_dir / str(txt_output_dir.name + ".md")
        with json_file.open() as stream:
            extracted_json = json.loads(stream.read())
        logging.info(f"Targeting '{target_element}' elements within '{json_file.resolve()}'.")
        
        _iterate_through_nested_dicts(extracted_json, txt_output, md_output, target_element)
        logging.info(f"Extracting text, converting tables and processing output.")
        logging.info(f"Creating '{txt_output.resolve()}'.")
        logging.info(f"Creating '{md_output.resolve()}'.")

def _iterate_through_nested_dicts(nested_dict, output_file_txt, output_file_md, target_element):
    """
    Recursively iterates through a dictionary and targets all "Text" keys and 
    their values to write to an output file.

    This sub function is called on the JSON files which are found by the function 
    "extract_text_from_json()".

    :param nested_dict: A JSON dictionary.
    :param output_file: File to output targeted values to.
    """
    keys_list = list(nested_dict.keys())
    values_list = list(nested_dict.values())
    path_text_pairs = list()
    csv_list = list()
    for key,value in nested_dict.items():
        if key == "filePaths":
            for file in value:
                if str(file).endswith(".csv"):
                    csv_list.append(file)

        if key == target_element:
            text_index = keys_list.index(key)
            path_index = keys_list.index("Path")
            temp_tuple = (values_list[path_index], values_list[text_index])
            path_text_pairs.append(temp_tuple)
            with open(output_file_txt, "a") as stream:
                stream.write(str(values_list[text_index]) + "\n")               # Swap with below after testing.
                # stream.write(str(keys_list[path_index]) + " : " + str(values_list[path_index]) + "\n")
                # stream.write(str(keys_list[text_index]) + " : " + str(values_list[text_index]) + "\n\n")
        elif isinstance(value, dict):
            _iterate_through_nested_dicts(value, output_file_txt, output_file_md, target_element)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    _iterate_through_nested_dicts(item, output_file_txt, output_file_md, target_element)
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            _iterate_through_nested_dicts(item, output_file_txt, output_file_md, target_element)
    _create_md_tables(csv_list, output_file_txt)
    _phase_one(path_text_pairs, output_file_md)

def _create_md_tables(csv_list, output_file_txt):
    for csv_file in csv_list:
        # print(csv_file)
        # print(output_file_txt)
        # txt_path = Path(output_file_txt)
        split_file_path = str(csv_file).rsplit("/")
        for item in split_file_path:
            if item.endswith(".csv"):
                csv_name = item
        output_dir = Path(output_file_txt).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        csv_output = output_dir / csv_name.replace(".csv", ".md")
        input_dir = str(output_dir).replace("extracted-content", "json-schema")
        input_path = Path(input_dir + "/" + csv_file)
        df = pd.read_csv(input_path, engine="python")
        with open(csv_output, "w") as stream:
            df.fillna("", inplace=True)
            df.to_markdown(buf=stream, tablefmt="github")




################################################################################
# PHASE ONE
################################################################################
def _phase_one(path_text_pairs, output_file_md):
    headings = ["Title"]
    paragraphs = ["P", "LBody", "ParagraphSpan", "Span", "StyleSpan"]
    lists = ["L"]
    table_headers = ["Table"]
    table_rows = ["TR"]
    table_data = ["TD"]
    unwanted = ["Aside"]
    phase_one = []

    for i in range(0, 101):
        headings.append(f"H{i}")
        paragraphs.append(f"P[{i}]")
        lists.append(f"LI[{i}]")
        # table_headers.append(f"TH[{i}]")
        table_headers.append(f"Table[{i}]")
        table_rows.append(f"TR[{i}]")
        table_data.append(f"TD[{i}]")
    # tr_val = None
    for (path, text) in path_text_pairs:
        split_path_list = path.split("/")
        # print(split_path_list)
        for item in split_path_list:
            if item in headings:
                temp_tuple = f"\n## {text}\n"
                phase_one.append(temp_tuple)
                break
            if item in lists:
                if "*" in text:
                    break
                if "◈" in text:
                    break
                if "-" == text:
                    break
                temp_tuple = f"- {text}\n"
                phase_one.append(temp_tuple)
                break
            if item in paragraphs:
                temp_tuple = f"{text} "
                phase_one.append(temp_tuple)
                break
            if item in table_headers:
                temp_tuple = f"\n{item} GOESHEREGOESHEREGOESHEREGOESHERE\n"
                phase_one.append(temp_tuple)
                break
    _phase_two_three_four(phase_one, output_file_md)
    

def _phase_two_three_four(phase_one,output_file_md):
    ############################################################################
    ############################################################################
    phase_two = []
    md_dir = Path(output_file_md).parent
    md_files = list(md_dir.rglob("fileoutpart*.md"))
    temp_file = Path(output_file_md).with_name("TEMP.md")
    with open(temp_file, "a") as stream:
        stream.writelines(phase_one)
    with open(temp_file, "r") as stream:
        dup_lines = stream.readlines()
    for line in dup_lines:
        # line = line.strip()
        if line not in phase_two:
            phase_two.append(line)
    with open(temp_file, "w") as stream:
        stream.writelines("".join(phase_two))
    ############################################################################
    ############################################################################
    phase_three = []
    with open(temp_file, "r") as stream:
        whitespace_lines = stream.readlines()
    for line in whitespace_lines:        
        if line not in phase_three and line.startswith("## "):
            temp_string = f"{line}\n"
            phase_three.append(temp_string)
        else:
            phase_three.append(line)
    with open(temp_file, "w") as stream:
        stream.writelines("".join(phase_three))
    ############################################################################
    ############################################################################
    phase_four = []
    with open(temp_file, "r") as stream:
        table_lines = stream.readlines()
    for line in table_lines:        
        if "GOESHEREGOESHEREGOESHEREGOESHERE" in line:
            tab_file = md_files.pop(-1)
            with open(tab_file, "r") as stream:
                tab_string = stream.read()
            phase_four.append("\n\n")
            phase_four.append(tab_string)
            phase_four.append("\n\n\n")
            continue
        else:
            phase_four.append(line)
    with open(output_file_md, "w") as stream:
        stream.writelines("".join(phase_four))
    ############################################################################
    ############################################################################

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
        images_path = Path(input_path).with_stem("extracted-content") / pdf_file.stem / "converted-pages"
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
        for sub_dir in directory.iterdir():
            if sub_dir.stem == "converted-pages":
                images_file_list = sorted(Path(directory).rglob(f"*{format}"))
                for item in images_file_list:
                    split_name = item.name.split("_page_")
                    txt_file_dir = f"{input_path}/{split_name[0]}"
                    txt_file_path = f"{txt_file_dir}/{split_name[0]}-IMAGE-OCR.txt"
                    Path(txt_file_dir).mkdir(parents=True, exist_ok=True)
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

def extract_images_from_pdf(input_path):
    input_path = Path(input_path)
    pdf_file_list = sorted(Path(input_path).rglob(f"*.pdf"))
    for pdf in pdf_file_list:
        doc = fitz.open(pdf)
        image_dir = f"{input_path.with_name('extracted-content')}/{pdf.stem}/extracted-images"
        Path(image_dir).mkdir(parents=True, exist_ok=True)
        for page in range(len(doc)):
            for img in doc.get_page_images(page):
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                if pix.n - pix.alpha < 4:
                    # this is GRAY or RGB
                    pix.save(f"{image_dir}/p{page}-{xref}.png")
                else:
                    # CMYK: convert to RGB first
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    pix1.save(f"{image_dir}/p{page}-{xref}.png")
                    pix1 = None
                pix = None

def extract_tables_from_pdf(input_pdf, start, end, page_number=0, table_number=1):
    """
    After reading a page:

    (1) search the strings that encapsulate our table
    (2) from coordinates of those string occurences, we define the surrounding
        rectangle. We use zero or large numbers to specify "no limit".
    (3) call ParseTab to get the parsed table
    
    The ParseTab function parses tables contained in a page of a PDF
    (or OpenXPS, EPUB) file and passes back a list of lists of strings
    that represents the original table in matrix form.
    """
    input_pdf = Path(input_pdf)
    doc = fitz.Document(input_pdf.resolve())
    page = doc.load_page(page_number)
    search_a = page.search_for(start, hit_max = 1)
    if not search_a:
        raise ValueError("The top delimiter was not found, exiting.")
    rect1 = search_a[0]  # the rectangle that surrounds the search string
    ymin = rect1.y1     # table starts below this value
    search_b = page.search_for(end, hit_max = 1)
    if not search_b:
        logging.warning("The bottom delimiter was not found - using end of page instead.")
        ymax = 99999
    else:
        rect2 = search_b[0]  # the rectangle that surrounds the search string
        ymax = rect2.y0     # table ends above this value
    if not ymin < ymax:     # something was wrong with the search strings
        raise ValueError("Something went wrong. The bottom delimiter is higher than the top.")
    table = parse_tab.parse_tab(page, [0, ymin, 9999, ymax])   
    csv_name = Path(f"{input_pdf.stem}-page-{page_number + 1}-table-{table_number}.csv")
    csv_dir = Path(f"../test/'extracted-content/{input_pdf.stem}/extracted-tables")
    Path(csv_dir).mkdir(parents=True, exist_ok=True)
    csv_path = csv_dir / csv_name
    with open(csv_path, "w") as stream:
        stream.write(start + "\n")
        for value in table:
            stream.write("|".join(value) + "\n")