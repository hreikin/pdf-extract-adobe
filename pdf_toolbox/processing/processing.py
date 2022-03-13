import logging

from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
from pathlib import Path

def split_all_pages_pdf(input_file):
    """Splits a PDF into individual pages."""
    input_file = Path(input_file).resolve()
    output_dir = Path("../test/processing/split/" + input_file.name.strip(".pdf") + "-PAGES/").resolve()
    input_pdf = PdfFileReader(open(input_file, "rb"))
    total_pages = input_pdf.getNumPages()
    logging.info(f"The file '{input_file.name}' has {total_pages} pages to split.")
    logging.info(f"Output directory is '{output_dir}'.")
    logging.info("Splitting pages now.")
    page_num = 0
    while page_num < total_pages:
        pypdf_writer = PdfFileWriter()
        pypdf_writer.addPage(input_pdf.getPage(page_num))
        page_num += 1
        page_name = input_file.name.strip(".pdf") + f"-PAGE-{page_num}.pdf"
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        output_path = output_dir / page_name
        with open(output_path, "wb") as stream:
            pypdf_writer.write(stream)
        logging.debug(f"Splitting page number {page_num}.")
    logging.info(f"Success, {page_num}/{total_pages} pages split from '{input_file.name}'.")

def append_pdf(input_one, input_two):
    """Appends one PDF on to the end of another."""
    merger = PdfFileMerger()
    input_one = Path(input_one).resolve()
    input_two = Path(input_two).resolve()
    output_dir = Path("../test/processing/merged/").resolve()
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    output_name = f"{input_one.stem}-{input_two.stem}-MERGED.pdf"
    output_path = output_dir / output_name
    pdf_one = open(input_one, "rb")
    pdf_two = open(input_two, "rb")
    merger.append(pdf_one)
    merger.append(pdf_two)
    logging.info(f"Merging '{input_one.name}' and '{input_two.name}'")
    merged_file = open(output_path, "wb")
    merger.write(merged_file)
    logging.info(f"Success, merged file available at '{output_path}'.")

def overlay(input_file, overlay_file):
    """Overlays one PDF onto another, useful for watermarking."""
    input_file = Path(input_file).resolve()
    output_dir = Path("../test/processing/overlay/")
    output_file = output_dir.resolve() / f"{input_file.stem}-OVERLAY.pdf"
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    overlay = PdfFileReader(overlay_file)
    overlay_page = overlay.getPage(0)
    pdf = PdfFileReader(str(input_file))
    pdf_writer = PdfFileWriter()
    for page in range(pdf.getNumPages()):
        pdf_page = pdf.getPage(page)
        pdf_page.mergePage(overlay_page)
        pdf_writer.addPage(pdf_page)
    with open(output_file, 'wb') as stream:
        pdf_writer.write(stream)
