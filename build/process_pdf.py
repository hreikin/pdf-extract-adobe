import logging

from PyPDF2 import PdfFileWriter, PdfFileReader
from pathlib import Path

def split_all_pages(input_file):
    input_file = Path(input_file).resolve()
    output_dir = Path("../test/pypdf2/" + input_file.name.strip(".pdf") + "-PAGES/").resolve()
    input_pdf = PdfFileReader(open(input_file, "rb"))
    total_pages = input_pdf.getNumPages()
    logging.info(f"The file '{input_file.name}' has {total_pages} pages to split.")
    logging.info(f"Output directory is '{output_dir}'.")
    logging.info("Splitting pages now.")
    page_num = 0
    while page_num <= total_pages - 1:
        pypdf_writer = PdfFileWriter()
        pypdf_writer.addPage(input_pdf.getPage(page_num))
        page_num += 1
        page_name = input_file.name.strip(".pdf") + f"-page-{page_num}.pdf"
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        output_path = str(output_dir) + page_name
        with open(output_path, "wb") as stream:
            pypdf_writer.write(stream)
        logging.info(f"{page_num}")
    logging.info(f"Success, {page_num} pages split from '{input_file.name}'.")








