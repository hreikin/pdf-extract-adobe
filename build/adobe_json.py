import utilities, json_to_sqlite

import logging, json

from pathlib import Path

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

def extract_pdf_adobe(source_path):
    """
    This function recursively finds all PDF files within a given directory and 
    then calls the sub function "_extract_all_from_pdf()" on all that are found.

    :param source_path: A directory containing PDF files.
    """
    zip_path = Path(source_path).with_stem("json-zips")
    pdf_file_list = sorted(Path(source_path).rglob("*.pdf"))
    pdf_amount = len(pdf_file_list)
    logging.info(f"Found {pdf_amount} PDF files, creating individual API requests.")
    for pdf in pdf_file_list:
        _create_adobe_request(pdf)
    logging.info("Extracting JSON Schema.")
    utilities.extract_from_zip(zip_path)
    # Leave the below commented out while testing using the "main.py" file.
    # logging.info("Manipulating Json and creating SQLite tables.")
    # json_to_sqlite.split_main_json_file(zip_path.resolve().with_stem("json-schema"))

def _create_adobe_request(source_file):
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
        base_path = Path("..").resolve()
        source_file = Path(source_file).resolve()
        pdf_name = source_file.stem
        # Initial setup, create credentials instance.
        credentials = Credentials.service_account_credentials_builder() \
            .from_file(base_path / "pdfservices-api-credentials.json") \
            .build()
        # Create client config instance with custom time-outs.
        client_config = ClientConfig.builder().with_connect_timeout(10000).with_read_timeout(40000).build()
        # Create an ExecutionContext using credentials and create a new operation instance.
        execution_context = ExecutionContext.create(credentials, client_config)
        extract_pdf_operation = ExtractPDFOperation.create_new()
        # Set operation input from a source file.
        source = FileRef.create_from_local_file(source_file)
        extract_pdf_operation.set_input(source)
        # Build ExtractPDF options and set them into the operation, an example 
        # with all options is below.
        # extract_pdf_options: ExtractPDFOptions = ExtractPDFOptions.builder() \
        #     .with_elements_to_extract([ExtractElementType.TEXT, ExtractElementType.TABLES]) \
        #     .with_get_char_info(True) \
        #     .with_table_structure_format(TableStructureType.CSV) \
        #     .with_elements_to_extract_renditions([ExtractRenditionsElementType.FIGURES, ExtractRenditionsElementType.TABLES]) \
        #     .with_include_styling_info(True) \
        #     .build()
        extract_pdf_options: ExtractPDFOptions = ExtractPDFOptions.builder() \
            .with_elements_to_extract([ExtractElementType.TEXT, ExtractElementType.TABLES]) \
            .with_table_structure_format(TableStructureType.CSV) \
            .with_elements_to_extract_renditions([ExtractRenditionsElementType.FIGURES, ExtractRenditionsElementType.TABLES]) \
            .build()
        extract_pdf_operation.set_options(extract_pdf_options)
        # Execute the operation.
        result: FileRef = extract_pdf_operation.execute(execution_context)
        # Save the result to the specified location.
        result.save_as(base_path / f"test/json-zips/{pdf_name}.zip")
    except (ServiceApiException, ServiceUsageException, SdkException):
        logging.exception(f"Exception encountered while executing operation on '{source_file}'.")
        logging.info(f"Retrying operation on '{source_file}'.")
        _create_adobe_request(source_file)

def create_pdf_url_list():
    out_path = Path("../test/").resolve()
    out_file = out_path / "pdf-urls.txt"
    with open("pdf-urls.jl") as stream:
        pdf_url_file = stream.readlines()
    pdf_url_dict = {}
    count = 0
    for line in pdf_url_file:
        json_line = json.loads(line)
        # print(json_line)
        for k, v in json_line.items():
            if k == "original_filename":
                pdf_url_dict[v] = str(json_line["page"])
    for k, v in pdf_url_dict.items():
        with open(out_file, "a") as stream:
            stream.write(k + "\n")
            stream.write(v + "\n")
            stream.write("\n")