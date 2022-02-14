import parse_tab
import logging, json, pytesseract, fitz
import pandas as pd

from pathlib import Path
from PIL import Image

def target_element_in_json(schema_source, target_element):
    """
    Recursively finds all JSON files within a directory, iterates through the 
    dictionary and converts any necessary tables before finally converting the 
    extracted content to markdown and integrating it with the converted tables.
    """
    json_file_list = Path(schema_source).rglob("*.json")
    out_dir = Path(schema_source).with_stem("extracted-content").resolve()
    logging.info("Extracting JSON content.")
    for json_file in json_file_list:
        path_text_pairs = list()
        csv_list = list()
        in_dir = Path(schema_source + json_file.parent.name).resolve()
        base_dir = out_dir / json_file.parent.name
        txt_dir = base_dir / "confidence"
        tab_dir = base_dir / "tables"
        txt_dir.mkdir(parents=True, exist_ok=True)
        json_txt = txt_dir / str(base_dir.name + "-EXTRACTED-JSON.txt")
        md_out = base_dir / str(txt_dir.parent.name + ".md")
        with json_file.open() as stream:
            json_dict = json.loads(stream.read())
        logging.info(f"Targeting '{target_element}' elements within '{json_file.resolve()}'.")
        _iterate_through_nested_dicts(json_dict, target_element, json_txt, path_text_pairs, csv_list, in_dir)
        if len(csv_list) > 0:
            tab_dir.mkdir(parents=True, exist_ok=True)
            logging.info("Converting found tables.")
            _create_md_tables(csv_list, tab_dir)
        logging.info(f"Creating '{md_out}'.")
        _md_conversion(path_text_pairs, md_out)
    logging.info("Cleaning up temp files.")
    temp_files = out_dir.rglob("TEMP.md")
    for item in temp_files:
        Path(item).unlink()

def _iterate_through_nested_dicts(nested_dict, txt_out, path_text_pairs, csv_list, in_dir):
    """
    Iterates through a dictionary targeting ".csv" files and "Text" entries 
    within. If a list or dictionary is encountered this function is recursively 
    called. Once all recursive functions have completed the "csv_list" and 
    "path_text_pairs" are returned for use in the next functions.
    """
    keys_list = list(nested_dict.keys())
    values_list = list(nested_dict.values())
    for key,value in nested_dict.items():
        if key == "filePaths":
            for file in value:
                if str(file).endswith(".csv"):
                    csv_list.append(in_dir / file)
        if key == "Text":
            text_index = keys_list.index(key)
            path_index = keys_list.index("Path")
            temp_tuple = (values_list[path_index], values_list[text_index])
            path_text_pairs.append(temp_tuple)
            with open(txt_out, "a") as stream:
                stream.write(str(values_list[text_index]) + "\n")               # Swap with below after testing.
                # stream.write(str(keys_list[path_index]) + " : " + str(values_list[path_index]) + "\n")
                # stream.write(str(keys_list[text_index]) + " : " + str(values_list[text_index]) + "\n\n")
        elif isinstance(value, dict):
            _iterate_through_nested_dicts(value, txt_out, path_text_pairs, csv_list, in_dir)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    _iterate_through_nested_dicts(item, txt_out, path_text_pairs, csv_list, in_dir)
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            _iterate_through_nested_dicts(item, txt_out, path_text_pairs, csv_list, in_dir)
    return csv_list, path_text_pairs

def _create_md_tables(csv_list, tab_dir):
    """
    Converts found ".csv" tables into Github markdown formatting using Pandas.
    """
    for csv_file in csv_list:
        tab_name = Path(csv_file).with_suffix(".md").name
        md_out = tab_dir / tab_name
        df = pd.read_csv(csv_file, engine="python")
        with open(md_out, "w") as stream:
            df.fillna("", inplace=True)
            df.to_markdown(buf=stream, tablefmt="github")

################################################################################
# Format targeted "Text" items with markdown based on Path value.
################################################################################
def _md_conversion(path_text_pairs, md_out):
    """
    Applies markdown formatting to the "Text" values based on the value 
    determined from the "Path" and then adds the entry to a new list for further 
    processing.
    """
    headings = ["Title"]
    paragraphs = ["P", "LBody", "ParagraphSpan", "Span", "StyleSpan"]
    lists = ["L"]
    table_headers = ["Table"]
    phase_one = []

    for i in range(0, 101):
        headings.append(f"H{i}")
        paragraphs.append(f"P[{i}]")
        lists.append(f"LI[{i}]")
        table_headers.append(f"Table[{i}]")
    for (path, text) in path_text_pairs:
        split_path_list = path.split("/")
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
    _processing(phase_one, md_out)
    
def _processing(phase_one, md_out):
    """
    Processes the markdown file before creating the final output. This removes 
    duplicate lines, applies extra whitespace and replaces the table entries in 
    the list with the relevant table before creating the final markdown output.
    """
################################################################################
# Variables.
################################################################################
    phase_two = []
    phase_three = []
    phase_four = []
    md_dir = Path(md_out).parent
    md_files = list(md_dir.rglob("fileoutpart*.md"))
    temp_file = Path(md_out).with_name("TEMP.md")
################################################################################
# Remove duplicate lines.
################################################################################
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
################################################################################
# Applying extra whitespace.
################################################################################
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
################################################################################
# Replacing table entries with the relevant converted table.
################################################################################
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
################################################################################
# Create final file.
################################################################################
    with open(md_out, "w") as stream:
        stream.writelines("".join(phase_four))

def split_all_pages_into_image(input_path, format):
    """
    Recursively finds all PDF files within a given directory and converts each 
    page of each PDF to an image using PyMuPDF. 
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
        for page in doc:
            logging.debug(f"Image created at '{images_path}/{image_name}{page.number}{format}'.")
            pix = page.get_pixmap(matrix=zoom_matrix)
            pix.save(f"{images_path}/{image_name}{page.number}{format}")

def ocr_images_for_text(input_path, format):
    """
    Recursively finds all images of the given format and performs OCR on them to 
    create a text file containing the infomation that was found.
    """
    input_path = Path(input_path)
    for directory in input_path.iterdir():
        for sub_dir in directory.iterdir():
            if sub_dir.stem == "converted-pages":
                images_file_list = sorted(Path(directory).rglob(f"*{format}"))
                for item in images_file_list:
                    split_name = item.name.split("_page_")
                    txt_file_dir = f"{input_path}/{split_name[0]}/confidence"
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
    ymin = rect1.y1      # table starts below this value
    search_b = page.search_for(end, hit_max = 1)
    if not search_b:
        logging.warning("The bottom delimiter was not found - using end of page instead.")
        ymax = 99999
    else:
        rect2 = search_b[0]  # the rectangle that surrounds the search string
        ymax = rect2.y0      # table ends above this value
    if not ymin < ymax:      # something was wrong with the search strings
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