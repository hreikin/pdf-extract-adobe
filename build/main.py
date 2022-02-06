import adobe_json, confidence, extraction, processing
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
# zip_source = "../test/json-zips/"
# logging.info("Extracting JSON Schema from zip files.")
# utilities.extract_from_zip(zip_source)

# Targets "Text" entries from the Json Schema and adds them to a file for each pdf.
schema_source = "../test/json-schema/"
target_element = "Text"
logging.info("Targeting 'Text' entries from the JSON Schema.")
extraction.target_element_in_json(schema_source, target_element)

# Convert PDF files to images for OCR/accuracy check.
pdf_path = "../test/pdfs/"
image_format = ".png"
logging.info("Converting PDF files to images.")
extraction.split_all_pages_into_image(pdf_path, image_format)

# Run the converted pdf images through OCR and create a text file for each one as output.
input_path = "../test/extracted-content/"
image_format = ".png"
logging.info("Running the converted images through OCR.")
extraction.ocr_images_for_text(input_path, image_format)

# Confidence Check
input_path = "../test/extracted-content/"
logging.info("Performing basic confidence check.")
confidence.confidence_check_text(input_path)
logging.info("Process complete, exiting.")

# Extract text from PDF
pdf_path = "../test/pdfs/"
extraction.extract_text_from_pdf(pdf_path)

# Extract images from PDF
pdf_path = "../test/pdfs/"
extraction.extract_images_from_pdf(pdf_path)

# # Extract tables from PDF - NOT WORKING
# pdf_path = "../test/pdfs/"
# extraction.extract_tables_from_pdf(pdf_path)

# Split all PDF pages
pdf_file = "../test/pdfs/Daresbury_labs_CS.1.pdf"
processing.split_all_pages_pdf(pdf_file)

# Merge two PDF files.
file_one = "../test/pdfs/Daresbury_labs_CS.1.pdf"
file_two = "../test/pdfs/Sputtering-Targets.pdf"
processing.append_pdf(file_one, file_two)

# Overlay PDF with another.
file_one = "../test/pdfs/Daresbury_labs_CS.1.pdf"
file_two = "../test/pdfs/Sputtering-Targets.pdf"
processing.overlay(file_one, file_two)