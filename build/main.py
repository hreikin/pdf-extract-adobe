import adobe_json, confidence, extraction, processing, json_to_sqlite, utilities, convert
import logging

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

# Creates Json Schema zip file with Adobe API.
source_path = "../test/pdfs/"
logging.info("Creating JSON Schema with Adobe API.")
adobe_json.extract_pdf_adobe(source_path)

# # Extracts Json Schema from zip file. Automatically called after the API 
# # requests are complete. Can be used on its own.
# zip_source = "../test/zips/"
# logging.info("Extracting JSON Schema from zip files.")
# utilities.extract_from_zip(zip_source)

# Creates list of PDF/URL pairs.
logging.info("Creating PDF/URL list.")
adobe_json.create_pdf_url_list()

# Splits the main Json Schema file into parts based on the top-level keys in the 
# file and then targets "Text", "filePaths", "Path" and "Page" values from 
# within the "elements.json" file and inserts it into an SQLite DB.
src = "../test/json/"
logging.info("Manipulating Json and creating SQLite tables.")
json_to_sqlite.split_main_json_file(src)

# Takes data from SQLite DB and applies markdown formatting to it before writing 
# to a file.
path = "../test/json/Beam-Profile-Measuring-System/"
convert.convert_db_markdown(path)
path = "../test/json/Daresbury_labs_CS.1/"
convert.convert_db_markdown(path, with_imgs=False)
path = "../test/json/Sputtering-Targets/"
convert.convert_db_markdown(path)
path = "../test/json/Starter-Kit-Princeton-Scientific/"
convert.convert_db_markdown(path)
path = "../test/json/WS22/"
convert.convert_db_markdown(path)

# Convert PDF files to images for OCR/accuracy check.
pdf_path = "../test/pdfs/"
image_format = ".png"
logging.info("Converting PDF files to images.")
extraction.convert_pages_into_image(pdf_path, image_format)

# Run the converted pdf images through OCR and create a text file for each one as output.
input_path = "../test/converted/"
logging.info("Running the converted images through OCR.")
extraction.ocr_images_for_text_confidence(input_path)

# Extract text from PDF with PyMuPDF.
pdf_path = "../test/pdfs/"
extraction.extract_text_from_pdf_confidence(pdf_path)

# Confidence Check
input_path = "../test/confidence/"
logging.info("Performing basic confidence check.")
confidence.confidence_check_text(input_path)

# Extract images from PDF
pdf_path = "../test/pdfs/"
extraction.extract_images_from_pdf(pdf_path)
logging.info("Process complete, exiting.")

# # Split all PDF pages
# pdf_file = "../test/pdfs/Daresbury_labs_CS.1.pdf"
# processing.split_all_pages_pdf(pdf_file)

# # Merge two PDF files.
# file_one = "../test/pdfs/Daresbury_labs_CS.1.pdf"
# file_two = "../test/pdfs/Sputtering-Targets.pdf"
# processing.append_pdf(file_one, file_two)

# # Overlay PDF with another.
# file_one = "../test/pdfs/Daresbury_labs_CS.1.pdf"
# file_two = "../test/pdfs/Sputtering-Targets.pdf"
# processing.overlay(file_one, file_two)

# # Extract tables from PDF - MANUAL ONLY, might be a way to automate with a list.
# pdf_path = "../test/pdfs/Sputtering-Targets.pdf"
# start = "Metals "
# end = "mmmmmmmm"
# extraction.extract_tables_from_pdf(pdf_path, start, end)
# pdf_path = "../test/pdfs/Sputtering-Targets.pdf"
# start = " "
# end = "Other materials"
# page_num = 1
# table_num = 2
# extraction.extract_tables_from_pdf(pdf_path, start, end, page_number=page_num, table_number=table_num)