import logging, os.path, zipfile, os, json, pytesseract

from PIL import Image
from pdf2image import convert_from_path

from adobe.pdfservices.operation.auth.credentials import Credentials
from adobe.pdfservices.operation.client_config import ClientConfig
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, ServiceUsageException, SdkException
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_pdf_options import ExtractPDFOptions
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_element_type import ExtractElementType
from adobe.pdfservices.operation.execution_context import ExecutionContext
from adobe.pdfservices.operation.io.file_ref import FileRef
from adobe.pdfservices.operation.pdfops.extract_pdf_operation import ExtractPDFOperation
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_renditions_element_type import ExtractRenditionsElementType
from adobe.pdfservices.operation.pdfops.options.extractpdf.table_structure_type import TableStructureType

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

def extract_pdf_adobe(source_path):
    for root, dirnames, filenames in os.walk(source_path):
        for filename in filenames:
            _extract_all_from_pdf(filename)

def _extract_all_from_pdf(source_file):
    try:
        # get base path.
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pdf_name = source_file.rstrip(".pdf")

        # Initial setup, create credentials instance.
        credentials = Credentials.service_account_credentials_builder() \
            .from_file(base_path + "/pdfservices-api-credentials.json") \
            .build()

        # Create client config instance with custom time-outs.
        client_config = ClientConfig.builder().with_connect_timeout(10000).with_read_timeout(40000).build()

        # Create an ExecutionContext using credentials and create a new operation instance.
        execution_context = ExecutionContext.create(credentials, client_config)
        extract_pdf_operation = ExtractPDFOperation.create_new()

        # Set operation input from a source file.
        source = FileRef.create_from_local_file(base_path + "/test/pdfs/" + source_file)
        extract_pdf_operation.set_input(source)

        # Build ExtractPDF options and set them into the operation
        extract_pdf_options: ExtractPDFOptions = ExtractPDFOptions.builder() \
            .with_elements_to_extract([ExtractElementType.TEXT, ExtractElementType.TABLES]) \
            .with_get_char_info(True) \
            .with_table_structure_format(TableStructureType.CSV) \
            .with_elements_to_extract_renditions([ExtractRenditionsElementType.FIGURES, ExtractRenditionsElementType.TABLES]) \
            .with_include_styling_info(True) \
            .build()
        extract_pdf_operation.set_options(extract_pdf_options)

        # Execute the operation.
        result: FileRef = extract_pdf_operation.execute(execution_context)

        # Save the result to the specified location.
        result.save_as(base_path + f"/test/json-zips/{pdf_name}-Extracted-Json-Schema.zip")
    except (ServiceApiException, ServiceUsageException, SdkException):
        logging.exception("Exception encountered while executing operation")


def extract_json_from_zip(zip_source, output_path):
    # Extracts Json Schema from zip file.
    with os.scandir(zip_source) as file_list:
        for file in file_list:
            if zipfile.is_zipfile(file):
                dirname = file.name.rstrip(".zip")
                if not os.path.isdir(output_path):
                    os.makedirs(output_path, exist_ok=True)
                with zipfile.ZipFile(file) as item:
                    item.extractall(output_path + "/" + dirname)


def do_something_with_json(schema_source):
    # Targets "Text" entries from the Json Schema and adds them to a file.
    for root, dirnames, filenames in os.walk(schema_source):
        for filename in filenames:
            if filename.endswith(".json"):
                file = os.path.join(root, filename)
                txt_file = os.path.join(root, filename.replace(".json", ".txt"))
                with open(file, "r") as stream:
                    extracted_json = json.loads(stream.read())
                for item in extracted_json["elements"]:
                    for k, v in item.items():
                        if k == "Text":
                            with open(txt_file, "a") as stream:
                                stream.write(v + "\n")

def convert_pdf_to_image(input_path, output_path, format):
    for root, dirnames, filenames in os.walk(input_path):
        for filename in filenames:
            image_name = filename.rstrip(".pdf") + "_page_"
            images_path = output_path + "/" + filename.rstrip(".pdf") + "/"
            if not os.path.isdir(images_path):
                os.makedirs(images_path, exist_ok=True)
            convert_from_path(root + "/" + filename, output_folder=images_path, output_file=image_name, thread_count=8, fmt=format)

def ocr_converted_pdf_images(input_path, output_path):
    with os.scandir(input_path) as dirs_list:
        for directory in dirs_list:
            for root, dirnames, filenames in os.walk(directory):
                split_filenames = filenames[0].split("_page_")
                txt_file_name = split_filenames[0] + "-ocr.txt"
                txt_file_path = output_path + "/" + txt_file_name
                if not os.path.isdir(output_path):
                    os.makedirs(output_path, exist_ok=True)
                for filename in filenames:
                    image_file_path = root + "/" + filename
                    with open(txt_file_path, "a") as stream:
                        stream.write(pytesseract.image_to_string(Image.open(image_file_path)))