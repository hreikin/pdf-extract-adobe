import extraction, confidence
import os

# Creates Json Schema zip file with Adobe API.
source_path = os.path.realpath("../test/pdfs/")
print("Creating Json Schema zip files with Adobe API.")
extraction.extract_pdf_adobe(source_path)

# Extracts Json Schema from zip file.
zip_source = os.path.realpath("../test/json-zips/")
json_output = os.path.realpath("../test/json-schema/")
print("Extracting Json Schema from zip files.")
extraction.extract_json_from_zip(zip_source, json_output)

# Targets "Text" entries from the Json Schema and adds them to a file for each pdf.
schema_source = os.path.realpath("../test/json-schema/")
print("Targeting 'Text' entries from the Json Schema and adding them to a file for each pdf.")
confidence.extract_text_from_json(schema_source)

# Convert PDF files to images for OCR/accuracy check.
pdf_path = os.path.realpath("../test/pdfs/")
image_path = os.path.realpath("../test/converted-pdf-images/")
image_format = "png"
print("Converting PDF files to images for OCR/accuracy check.")
confidence.convert_pdf_to_image(pdf_path, image_path, image_format)

# Run the converted pdf images through OCR and create a text file for each one as output.
input_path = os.path.realpath("../test/converted-pdf-images/")
output_path = os.path.realpath("../test/json-schema/")
print("Running the converted PDF images through OCR to create a text file for each one as output.")
confidence.ocr_converted_pdf_images(input_path, output_path)

# Confidence Check
input_path = os.path.realpath("../test/json-schema/")
print("Performing basic confidence check.")
confidence.confidence_check_text(input_path)

# # Extract images from PDF for comparison
# input_path = os.path.realpath("../test/pdfs/")
# output_path = os.path.realpath("../test/extracted-images/")
# confidence.extract_images_from_pdf(input_path, output_path)