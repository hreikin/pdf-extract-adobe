import logging
import os.path
import zipfile, os, json

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

def extract_all_from_pdf(source_file):
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
        source = FileRef.create_from_local_file(base_path + "/test/" + source_file)
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
        result.save_as(base_path + f"/test/{pdf_name}-Extracted-Json-Schema.zip")
    except (ServiceApiException, ServiceUsageException, SdkException):
        logging.exception("Exception encountered while executing operation")


def extract_json_from_zip(json_source):
    # Extracts Json Schema from zip file.
    os.chdir(json_source)
    for file in os.listdir(json_source):
        if zipfile.is_zipfile(file):
            dirname = file.rstrip(".zip")
            output_path = os.path.join(json_source + "/json/" + dirname)
            if not os.path.isdir(output_path):
                os.makedirs(output_path, exist_ok=True)
            with zipfile.ZipFile(file) as item:
                item.extractall(output_path)


def do_something_with_json(schema_source):
    # Loads Json Schema and prints the output.
    for root, dirnames, filenames in os.walk(schema_source):
        for filename in filenames:
            if filename.endswith(".json"):
                file = os.path.join(root, filename)
                with open(file, "r") as stream:
                    extracted_json = json.loads(stream.read())
                for item in extracted_json["elements"][:]:
                    for k, v in item.items():
                        if k == "Text":
                            print(v)