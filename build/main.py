import extraction
import os, zipfile

source_path = "../test/"
# for root, dirnames, filenames in os.walk(source_path):
    # for filename in filenames:
        # All functions listed below work and currently output a zip file with 
        # the relevant data inside.
        # extraction.extract_all_from_pdf(filename)
        # extraction.extract_txt_from_pdf(filename)
        # extraction.extract_txt_from_pdf_with_custom_timeouts(filename)
        # extraction.extract_txt_table_info_from_pdf(filename)
        # extraction.extract_txt_table_info_with_char_bounds_from_pdf(filename)
        # extraction.extract_txt_table_info_with_figure_tables_rendition_from_pdf(filename)
        # extraction.extract_txt_table_info_with_rendition_from_pdf(filename)
        # extraction.extract_txt_table_info_with_table_structure_from_pdf(filename)
        # extraction.extract_txt_with_char_bounds_from_pdf(filename)
        # extraction.extract_txt_with_styling_info_from_pdf(filename)


        # Not currently working
        # extraction.extract_txt_from_pdf_with_in_memory_auth_credentials(filename)

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
