import logging, zipfile, os

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

# Logging for the adobe API
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

def extract_pdf_adobe(source_path):
    """
    This function walks through a given directory and in turn calls the sub 
    function "_extract_all_from_pdf()" on every PDF file found.

    :param source_path: A directory containing PDF files.
    """
    for root, dirnames, filenames in os.walk(source_path):
        for filename in filenames:
            if filename.endswith(".pdf"):
                _extract_all_from_pdf(filename)

def _extract_all_from_pdf(source_file):
    """
    Takes an input PDF file and builds a request which is sent to the Adobe PDF 
    Extract API. 
    
    This downloads a zip file containing the JSON Schema extracted from the 
    source file. This sub function is called on every PDF file in the source 
    directory by the "extract_pdf_adobe()" function.

    :param source_file: A PDF file.
    """
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
    """
    Finds all zip files within a source directory and unzips them to a given 
    output directory.

    :param zip_source: A directory containing zip files.
    :param output_path: The directory to extract the zip contents in to.
    """
    # Extracts Json Schema from zip file.
    with os.scandir(zip_source) as file_list:
        for file in file_list:
            if zipfile.is_zipfile(file):
                dirname = file.name.rstrip(".zip")
                if not os.path.isdir(output_path):
                    os.makedirs(output_path, exist_ok=True)
                with zipfile.ZipFile(file) as item:
                    item.extractall(output_path + "/" + dirname)