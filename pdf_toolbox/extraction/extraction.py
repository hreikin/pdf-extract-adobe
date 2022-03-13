import utils.constants
import logging, pytesseract, fitz
import pandas as pd

from pathlib import Path
from PIL import Image

def convert_pages_into_image(input_path, format):
    """Recursively finds all PDF files within a given directory and converts each 
    page of each PDF to an image using PyMuPDF."""
    # To get better resolution
    zoom_x = 2.0
    zoom_y = 2.0
    zoom_matrix = fitz.Matrix(zoom_x, zoom_y)
    pdf_file_list = Path(input_path).rglob("*.pdf")
    for pdf_file in pdf_file_list:
        logging.debug(f"Converting '{pdf_file.resolve()}'.")
        doc = fitz.open(pdf_file)
        image_name = pdf_file.stem + "_page_"
        images_path = utils.constants.converted_dir / "pages-converted-to-images" / pdf_file.stem
        Path(images_path).mkdir(parents=True, exist_ok=True)
        for page in doc:
            logging.debug(f"Image created at '{images_path}/{image_name}{page.number}{format}'.")
            pix = page.get_pixmap(matrix=zoom_matrix)
            pix.save(f"{images_path}/{image_name}{page.number}{format}")

def ocr_images_for_text_confidence(input_path, format=".png"):
    """Recursively finds all images of the given format and performs OCR on them 
    to create a text file containing the infomation that was found."""
    input_path = Path(input_path).resolve()
    for directory in input_path.iterdir():
        if directory.name == "pages-converted-to-images":
            for sub_dir in directory.iterdir():
                images_file_list = sorted(Path(sub_dir).rglob(f"*{format}"))
                for item in images_file_list:
                    split_name = item.name.split("_page_")
                    txt_file_path = Path(f"{utils.constants.confidence_dir}/{sub_dir.name}/{split_name[0]}-IMAGE-OCR.txt").resolve()
                    txt_file_path.parent.mkdir(parents=True, exist_ok=True)
                    logging.debug(f"Performing OCR on '{item.resolve()}'.")
                    logging.debug(f"Creating text output file at '{txt_file_path}'.")
                    ocr_string = pytesseract.image_to_string(Image.open(item))
                    with open(txt_file_path, "a") as stream:
                        stream.write(ocr_string)

def extract_text_from_pdf_confidence(input_path):
    """Extracts all text from all found PDF files using PyMuPDF for the 
    confidence check"""
    input_path = Path(input_path).resolve()
    pdf_file_list = sorted(Path(input_path).rglob(f"*.pdf"))
    for pdf in pdf_file_list:
        txt_file_path = Path(f"{utils.constants.confidence_dir}/{pdf.stem}/{pdf.stem}-PYMUPDF-TXT.txt").resolve()
        txt_file_path.parent.mkdir(parents=True, exist_ok=True)
        logging.debug(f"Extracting text from '{pdf.resolve()}'.")
        logging.debug(f"Creating text output file at '{txt_file_path}'.")
        with fitz.open(pdf) as doc:
            pdf_text = ""
            for page in doc:
                pdf_text += page.get_text()
        with open(txt_file_path, "a") as stream:
            stream.write(pdf_text)

def extract_images_from_pdf(input_path):
    """Extracts all images from all found PDF files using PyMuPDF."""
    input_path = Path(input_path).resolve()
    pdf_file_list = sorted(Path(input_path).rglob(f"*.pdf"))
    for pdf in pdf_file_list:
        doc = fitz.open(pdf)
        image_dir = Path(f"{utils.constants.extracted_dir}/{pdf.stem}/extracted-images").resolve()
        image_dir.mkdir(parents=True, exist_ok=True)
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
