import extraction
import os

# Creates Json Schema zip file with Adobe API.
source_path = "../test/"
for root, dirnames, filenames in os.walk(source_path):
    for filename in filenames:
        extraction.extract_all_from_pdf(filename)

# Extracts Json Schema from zip file.
json_source = os.path.realpath("../test/")
extraction.extract_json_from_zip(json_source)

# Loads Json Schema and prints the output.
schema_source = os.path.realpath("../test/json/")
extraction.do_something_with_json(schema_source)