import extraction
import os

source_path = "../test/"
for root, dirnames, filenames in os.walk(source_path):
    for filename in filenames:
        extraction.extract_txt_from_pdf(filename)

