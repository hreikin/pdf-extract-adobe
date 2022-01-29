import json
import extraction
import os, zipfile

# source_path = "../test/"
# for root, dirnames, filenames in os.walk(source_path):
#     for filename in filenames:
#         extraction.extract_all_from_pdf(filename)


# json_source = os.path.realpath("../test/")
# os.chdir(json_source)
# for file in os.listdir(json_source):
#     if zipfile.is_zipfile(file):
#         dirname = file.rstrip(".zip")
#         output_path = os.path.join(json_source + "/json/" + dirname)
#         if not os.path.isdir(output_path):
#             os.makedirs(output_path, exist_ok=True)
#         with zipfile.ZipFile(file) as item:
#             item.extractall(output_path)

schema_source = os.path.realpath("../test/json/")
for root, dirnames, filenames in os.walk(schema_source):
    for filename in filenames:
        if filename.endswith(".json"):
            file = os.path.join(root, filename)
            with open(file, "r") as stream:
                extracted_json = json.loads(stream.read())
            print(extracted_json)