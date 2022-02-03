import extraction, accuracy
import os

# Creates Json Schema zip file with Adobe API.
source_path = os.path.realpath("../test/pdfs/")
extraction.extract_pdf_adobe(source_path)

# Extracts Json Schema from zip file.
zip_source = os.path.realpath("../test/json-zips/")
json_output = os.path.realpath("../test/json-schema/")
extraction.extract_json_from_zip(zip_source, json_output)

# Targets "Text" entries from the Json Schema and adds them to a file for each pdf.
schema_source = os.path.realpath("../test/json-schema/")
accuracy.extract_text_from_json(schema_source)

# Convert PDF files to images for OCR/accuracy check.
pdf_path = os.path.realpath("../test/pdfs/")
image_path = os.path.realpath("../test/converted-pdf-images/")
image_format = "png"
accuracy.convert_pdf_to_image(pdf_path, image_path, image_format)

# Run the converted pdf images through OCR and create a text file for each one as output.
input_path = os.path.realpath("../test/converted-pdf-images/")
output_path = os.path.realpath("../test/json-schema/")
accuracy.ocr_converted_pdf_images(input_path, output_path)

# Accuracy Check
input_path = os.path.realpath("../test/json-schema/")
accuracy.accuracy_check(input_path)