import extraction.adobe_json, processing.processing, extraction.json_to_sqlite, utilities.utilities, conversion.convert, utilities.constants, extraction.extraction, extraction.confidence
import logging

from pathlib import Path

##################################### LOGS #####################################
# Initialize the logger and specify the level of logging. This will log "DEBUG" 
# and higher messages to file and log "INFO" and higher messages to the console.
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%d-%m-%y %H:%M:%S',
                    filename='debug.log',
                    filemode='w')

# Define a "handler" which writes "INFO" messages or higher to the "sys.stderr".
console = logging.StreamHandler()
console.setLevel(logging.INFO)

# Set a format which is simpler for console messages.
formatter = logging.Formatter('[%(asctime)s]: %(message)s', datefmt='%H:%M:%S')

# Tell the console "handler" to use this format.
console.setFormatter(formatter)

# Add the "handler" to the "root logger".
logging.getLogger('').addHandler(console)

################################################################################

new_headings = ["Title"]
for item in utilities.constants.headings:
    new_headings.append(item)
    for i in range(0, 101):
        new_headings.append(f"{item}[{i}]")

utilities.constants.headings = new_headings

# Creates Json Schema zip file with Adobe API.
source_path = "../src/pdfs/"
logging.info("Creating JSON Schema with Adobe API.")
extraction.adobe_json.extract_pdf_adobe(source_path)

# # Extracts Json Schema from zip file. Automatically called after the API 
# # requests are complete. Can be used on its own.
# zip_source = "../src/zips/"
# logging.info("Extracting JSON Schema from zip files.")
# utilities.utilities.extract_from_zip(zip_source)

# Creates list of PDF/URL pairs.
logging.info("Creating PDF/URL list.")
extraction.adobe_json.create_pdf_url_list()

# Splits the main Json Schema file into parts based on the top-level keys in the 
# file and then targets "Text", "filePaths", "Path" and "Page" values from 
# within the "elements.json" file and inserts it into an SQLite DB.
src = "../src/json/"
logging.info("Manipulating Json and creating SQLite tables.")
extraction.json_to_sqlite.split_main_json_file(src)

src_dir = Path(utilities.constants.json_dir).resolve()
for directory in src_dir.iterdir():
    conversion.convert.convert_db_markdown(directory.resolve())
    conversion.convert.convert_db_markdown(directory.resolve(), with_imgs=False)

# Convert PDF files to images for OCR/accuracy check.
pdf_path = "../src/pdfs/"
image_format = ".png"
logging.info("Converting PDF files to images.")
extraction.extraction.convert_pages_into_image(pdf_path, image_format)

# Run the converted pdf images through OCR and create a text file for each one as output.
input_path = "../src/converted/"
logging.info("Running the converted images through OCR.")
extraction.extraction.ocr_images_for_text_confidence(input_path)

# Extract text from PDF with PyMuPDF.
pdf_path = "../src/pdfs/"
extraction.extraction.extract_text_from_pdf_confidence(pdf_path)

# Confidence Check
input_path = "../src/confidence/"
logging.info("Performing basic confidence check.")
extraction.confidence.confidence_check_text(input_path)

# Extract images from PDF
pdf_path = "../src/pdfs/"
extraction.extraction.extract_images_from_pdf(pdf_path)
logging.info("Process complete, exiting.")

# # Split all PDF pages
# pdf_file = "../src/pdfs/Daresbury_labs_CS.1.pdf"
# processing.processing.split_all_pages_pdf(pdf_file)

# # Merge two PDF files.
# file_one = "../src/pdfs/Daresbury_labs_CS.1.pdf"
# file_two = "../src/pdfs/Sputtering-Targets.pdf"
# processing.processing.append_pdf(file_one, file_two)

# # Overlay PDF with another.
# file_one = "../src/pdfs/Daresbury_labs_CS.1.pdf"
# file_two = "../src/pdfs/Sputtering-Targets.pdf"
# processing.processing.overlay(file_one, file_two)