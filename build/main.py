import extraction
import os

# # Creates Json Schema zip file with Adobe API.
# source_path = os.path.realpath("../test/pdfs/")
# extraction.extract_pdf_adobe(source_path)

# Extracts Json Schema from zip file.
zip_source = os.path.realpath("../test/zips/")
json_output = os.path.realpath("../test/json/")
extraction.extract_json_from_zip(zip_source, json_output)

# Targets "Text" entries from the Json Schema and adds them to a file.
schema_source = os.path.realpath("../test/json/")
extraction.do_something_with_json(schema_source)

# Convert PDF files to images.
pdf_path = os.path.realpath("../test/pdfs/")
image_path = os.path.realpath("../test/images/")
image_format = "png"
extraction.convert_pdf_to_image(pdf_path, image_path, image_format)