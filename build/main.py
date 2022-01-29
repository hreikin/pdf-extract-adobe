import extraction
import os, zipfile

source_path = "../test/"
for root, dirnames, filenames in os.walk(source_path):
    for filename in filenames:
        extraction.extract_all_from_pdf(filename)


json_source = os.path.realpath("../output/")
os.chdir(json_source)
for file in os.listdir(json_source):
    if zipfile.is_zipfile(file):
        dirname = file.rstrip(".zip")
        output_path = os.path.join(json_source + "/" + dirname)
        if not os.path.isdir(output_path):
            os.mkdir(output_path)
        with zipfile.ZipFile(file) as item:
            item.extractall(output_path)
