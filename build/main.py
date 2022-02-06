import extraction, confidence, processing
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
logging.info("Creating JSON Schema zip files with Adobe API.")
extraction.extract_pdf_adobe(source_path)

# Extracts Json Schema from zip file.
zip_source = "../test/json-zips/"
json_output = "../test/json-schema/"
logging.info("Extracting JSON Schema from zip files.")
extraction.extract_from_zip(zip_source, json_output)

# Targets "Text" entries from the Json Schema and adds them to a file for each pdf.
schema_source = "../test/json-schema/"
output_path = "../test/confidence-check/"
logging.info("Targeting 'Text' entries from the JSON Schema.")
confidence.extract_text_from_json(schema_source, output_path)

# Convert PDF files to images for OCR/accuracy check.
pdf_path = "../test/pdfs/"
image_path = "../test/confidence-check/converted-images/"
image_format = "png"
logging.info("Converting PDF files to images.")
confidence.split_all_pages_image(pdf_path, image_path, image_format)

# Run the converted pdf images through OCR and create a text file for each one as output.
input_path = "../test/confidence-check/"
output_path = "../test/confidence-check/"
image_format = "png"
logging.info("Running the converted images through OCR.")
confidence.ocr_images(input_path, output_path, image_format)

# Confidence Check
input_path = "../test/confidence-check/"
logging.info("Performing basic confidence check.")
confidence.confidence_check_text(input_path)
logging.info("Process complete, exiting.")

pdf_file = "../test/pdfs/gce-core-rules-1.21.pdf"
processing.split_all_pages_pdf(pdf_file)

file_one = "../test/pdfs/Daresbury_labs_CS.1.pdf"
file_two = "../test/pdfs/Sputtering-Targets.pdf"
processing.append_pdf(file_one, file_two)