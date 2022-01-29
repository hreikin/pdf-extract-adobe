import logging
import os.path

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
        result.save_as(base_path + f"/output/{pdf_name}-Extracted-Json-Schema.zip")
    except (ServiceApiException, ServiceUsageException, SdkException):
        logging.exception("Exception encountered while executing operation")
	
def extract_txt_from_pdf(source_file):
    try:
        # get base path.
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pdf_name = source_file.rstrip(".pdf")

        # Initial setup, create credentials instance.
        credentials = Credentials.service_account_credentials_builder() \
            .from_file(base_path + "/pdfservices-api-credentials.json") \
            .build()

        # Create an ExecutionContext using credentials and create a new operation instance.
        execution_context = ExecutionContext.create(credentials)
        extract_pdf_operation = ExtractPDFOperation.create_new()

        # Set operation input from a source file.
        source = FileRef.create_from_local_file(base_path + "/test/" + source_file)
        extract_pdf_operation.set_input(source)

        # Build ExtractPDF options and set them into the operation
        extract_pdf_options: ExtractPDFOptions = ExtractPDFOptions.builder() \
            .with_element_to_extract(ExtractElementType.TEXT) \
            .build()
        extract_pdf_operation.set_options(extract_pdf_options)

        # Execute the operation.
        result: FileRef = extract_pdf_operation.execute(execution_context)

        # Save the result to the specified location.
        result.save_as(base_path + f"/output/{pdf_name}ExtractTextInfoFromPDF.zip")
    except (ServiceApiException, ServiceUsageException, SdkException):
        logging.exception("Exception encountered while executing operation")

def extract_txt_from_pdf_with_custom_timeouts(source_file):
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
            .with_element_to_extract(ExtractElementType.TEXT) \
            .build()
        extract_pdf_operation.set_options(extract_pdf_options)

        # Execute the operation.
        result: FileRef = extract_pdf_operation.execute(execution_context)

        # Save the result to the specified location.
        result.save_as(base_path + f"/output/{pdf_name}ExtractTextInfoFromPDFWithCustomTimeouts.zip")
    except (ServiceApiException, ServiceUsageException, SdkException):
        logging.exception("Exception encountered while executing operation")

def extract_txt_table_info_from_pdf(source_file):
    try:
        # get base path.
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pdf_name = source_file.rstrip(".pdf")

        # Initial setup, create credentials instance.
        credentials = Credentials.service_account_credentials_builder() \
            .from_file(base_path + "/pdfservices-api-credentials.json") \
            .build()

        # Create an ExecutionContext using credentials and create a new operation instance.
        execution_context = ExecutionContext.create(credentials)
        extract_pdf_operation = ExtractPDFOperation.create_new()

        # Set operation input from a source file.
        source = FileRef.create_from_local_file(base_path + "/test/" + source_file)
        extract_pdf_operation.set_input(source)

        # Build ExtractPDF options and set them into the operation
        extract_pdf_options: ExtractPDFOptions = ExtractPDFOptions.builder() \
            .with_element_to_extract(ExtractElementType.TEXT) \
            .with_element_to_extract(ExtractElementType.TABLES) \
            .build()
        extract_pdf_operation.set_options(extract_pdf_options)

        # Execute the operation.
        result: FileRef = extract_pdf_operation.execute(execution_context)

        # Save the result to the specified location.
        result.save_as(base_path + f"/output/{pdf_name}ExtractTextTableInfoFromPDF.zip")
    except (ServiceApiException, ServiceUsageException, SdkException):
        logging.exception("Exception encountered while executing operation")

def extract_txt_table_info_with_char_bounds_from_pdf(source_file):
    try:
        # get base path.
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pdf_name = source_file.rstrip(".pdf")

        # Initial setup, create credentials instance.
        credentials = Credentials.service_account_credentials_builder() \
            .from_file(base_path + "/pdfservices-api-credentials.json") \
            .build()

        # Create an ExecutionContext using credentials and create a new operation instance.
        execution_context = ExecutionContext.create(credentials)
        extract_pdf_operation = ExtractPDFOperation.create_new()

        # Set operation input from a source file.
        source = FileRef.create_from_local_file(base_path + "/test/" + source_file)
        extract_pdf_operation.set_input(source)

        # Build ExtractPDF options and set them into the operation
        extract_pdf_options: ExtractPDFOptions = ExtractPDFOptions.builder() \
            .with_elements_to_extract([ExtractElementType.TEXT, ExtractElementType.TABLES]) \
            .with_element_to_extract_renditions(ExtractRenditionsElementType.TABLES) \
            .with_get_char_info(True) \
            .build()
        extract_pdf_operation.set_options(extract_pdf_options)

        # Execute the operation.
        result: FileRef = extract_pdf_operation.execute(execution_context)

        # Save the result to the specified location.
        result.save_as(base_path + f"/output/{pdf_name}ExtractTextTableInfoWithCharBoundsFromPDF.zip")
    except (ServiceApiException, ServiceUsageException, SdkException):
        logging.exception("Exception encountered while executing operation")

def extract_txt_table_info_with_figure_tables_rendition_from_pdf(source_file):
    try:
        # get base path.
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pdf_name = source_file.rstrip(".pdf")

        # Initial setup, create credentials instance.
        credentials = Credentials.service_account_credentials_builder() \
            .from_file(base_path + "/pdfservices-api-credentials.json") \
            .build()

        # Create an ExecutionContext using credentials and create a new operation instance.
        execution_context = ExecutionContext.create(credentials)
        extract_pdf_operation = ExtractPDFOperation.create_new()

        # Set operation input from a source file.
        source = FileRef.create_from_local_file(base_path + "/test/" + source_file)
        extract_pdf_operation.set_input(source)

        # Build ExtractPDF options and set them into the operation
        extract_pdf_options: ExtractPDFOptions = ExtractPDFOptions.builder() \
            .with_elements_to_extract([ExtractElementType.TEXT, ExtractElementType.TABLES]) \
            .with_elements_to_extract_renditions([ExtractRenditionsElementType.TABLES,
                                                ExtractRenditionsElementType.FIGURES]) \
            .build()
        extract_pdf_operation.set_options(extract_pdf_options)

        # Execute the operation.
        result: FileRef = extract_pdf_operation.execute(execution_context)

        # Save the result to the specified location.
        result.save_as(base_path + f"/output/{pdf_name}ExtractTextTableWithFigureTableRendition.zip")
    except (ServiceApiException, ServiceUsageException, SdkException):
        logging.exception("Exception encountered while executing operation")

def extract_txt_table_info_with_rendition_from_pdf(source_file):
    try:
        # get base path.
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pdf_name = source_file.rstrip(".pdf")

        # Initial setup, create credentials instance.
        credentials = Credentials.service_account_credentials_builder() \
            .from_file(base_path + "/pdfservices-api-credentials.json") \
            .build()

        # Create an ExecutionContext using credentials and create a new operation instance.
        execution_context = ExecutionContext.create(credentials)
        extract_pdf_operation = ExtractPDFOperation.create_new()

        # Set operation input from a source file.
        source = FileRef.create_from_local_file(base_path + "/test/" + source_file)
        extract_pdf_operation.set_input(source)

        # Build ExtractPDF options and set them into the operation
        extract_pdf_options: ExtractPDFOptions = ExtractPDFOptions.builder() \
            .with_elements_to_extract([ExtractElementType.TEXT, ExtractElementType.TABLES]) \
            .with_element_to_extract_renditions(ExtractRenditionsElementType.TABLES) \
            .build()
        extract_pdf_operation.set_options(extract_pdf_options)

        # Execute the operation.
        result: FileRef = extract_pdf_operation.execute(execution_context)

        # Save the result to the specified location.
        result.save_as(base_path + f"/output/{pdf_name}ExtractTextTableWithTableRendition.zip")
    except (ServiceApiException, ServiceUsageException, SdkException):
        logging.exception("Exception encountered while executing operation")

def extract_txt_table_info_with_table_structure_from_pdf(source_file):
    try:
        # get base path.
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pdf_name = source_file.rstrip(".pdf")

        # Initial setup, create credentials instance.
        credentials = Credentials.service_account_credentials_builder() \
            .from_file(base_path + "/pdfservices-api-credentials.json") \
            .build()

        # Create an ExecutionContext using credentials and create a new operation instance.
        execution_context = ExecutionContext.create(credentials)
        extract_pdf_operation = ExtractPDFOperation.create_new()

        # Set operation input from a source file.
        source = FileRef.create_from_local_file(base_path + "/test/" + source_file)
        extract_pdf_operation.set_input(source)

        # Build ExtractPDF options and set them into the operation
        extract_pdf_options: ExtractPDFOptions = ExtractPDFOptions.builder() \
            .with_elements_to_extract([ExtractElementType.TEXT, ExtractElementType.TABLES]) \
            .with_element_to_extract_renditions(ExtractRenditionsElementType.TABLES) \
            .with_table_structure_format(TableStructureType.CSV) \
            .build()
        extract_pdf_operation.set_options(extract_pdf_options)

        # Execute the operation.
        result: FileRef = extract_pdf_operation.execute(execution_context)

        # Save the result to the specified location.
        result.save_as(base_path + f"/output/{pdf_name}ExtractTextTableWithTableStructure.zip")
    except (ServiceApiException, ServiceUsageException, SdkException):
        logging.exception("Exception encountered while executing operation")

def extract_txt_with_char_bounds_from_pdf(source_file):
    try:
        # get base path.
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pdf_name = source_file.rstrip(".pdf")

        # Initial setup, create credentials instance.
        credentials = Credentials.service_account_credentials_builder() \
            .from_file(base_path + "/pdfservices-api-credentials.json") \
            .build()

        # Create an ExecutionContext using credentials and create a new operation instance.
        execution_context = ExecutionContext.create(credentials)
        extract_pdf_operation = ExtractPDFOperation.create_new()

        # Set operation input from a source file.
        source = FileRef.create_from_local_file(base_path + "/test/" + source_file)
        extract_pdf_operation.set_input(source)

        # Build ExtractPDF options and set them into the operation
        extract_pdf_options: ExtractPDFOptions = ExtractPDFOptions.builder() \
            .with_element_to_extract(ExtractElementType.TEXT) \
            .with_get_char_info(True) \
            .build()
        extract_pdf_operation.set_options(extract_pdf_options)

        # Execute the operation.
        result: FileRef = extract_pdf_operation.execute(execution_context)

        # Save the result to the specified location.
        result.save_as(base_path + f"/output/{pdf_name}ExtractTextInfoWithCharBoundsFromPDF.zip")
    except (ServiceApiException, ServiceUsageException, SdkException):
        logging.exception("Exception encountered while executing operation")

def extract_txt_with_styling_info_from_pdf(source_file):
    try:
        # get base path.
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pdf_name = source_file.rstrip(".pdf")

        # Initial setup, create credentials instance.
        credentials = Credentials.service_account_credentials_builder() \
            .from_file(base_path + "/pdfservices-api-credentials.json") \
            .build()

        # Create an ExecutionContext using credentials and create a new operation instance.
        execution_context = ExecutionContext.create(credentials)
        extract_pdf_operation = ExtractPDFOperation.create_new()

        # Set operation input from a source file.
        source = FileRef.create_from_local_file(base_path + "/test/" + source_file)
        extract_pdf_operation.set_input(source)

        # Build ExtractPDF options and set them into the operation
        extract_pdf_options: ExtractPDFOptions = ExtractPDFOptions.builder() \
            .with_element_to_extract(ExtractElementType.TEXT) \
            .with_include_styling_info(True) \
            .build()
        extract_pdf_operation.set_options(extract_pdf_options)

        # Execute the operation.
        result: FileRef = extract_pdf_operation.execute(execution_context)

        # Save the result to the specified location.
        result.save_as(base_path + f"/output/{pdf_name}ExtractTextInfoWithStylingInfoFromPDF.zip")
    except (ServiceApiException, ServiceUsageException, SdkException):
        logging.exception("Exception encountered while executing operation")

def extract_txt_from_pdf_with_in_memory_auth_credentials(source_file):
    try:
        # get base path.
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pdf_name = source_file.rstrip(".pdf")

        # Initial setup, create credentials instance.
        credentials = Credentials.service_account_credentials_builder() \
            .with_client_id("client_id") \
            .with_client_secret("client_secret") \
            .with_organization_id("organization_id") \
            .with_account_id("account_id") \
            .with_private_key("private_key") \
            .build()

        # Create an ExecutionContext using credentials and create a new operation instance.
        execution_context = ExecutionContext.create(credentials)
        extract_pdf_operation = ExtractPDFOperation.create_new()

        # Set operation input from a source file.
        source = FileRef.create_from_local_file(base_path + "/test/" + source_file)
        extract_pdf_operation.set_input(source)

        # Build ExtractPDF options and set them into the operation
        extract_pdf_options: ExtractPDFOptions = ExtractPDFOptions.builder() \
            .with_element_to_extract(ExtractElementType.TEXT) \
            .build()
        extract_pdf_operation.set_options(extract_pdf_options)

        # Execute the operation.
        result: FileRef = extract_pdf_operation.execute(execution_context)

        # Save the result to the specified location.
        result.save_as(base_path + f"/output/{pdf_name}ExtractTextInfoFromPDFWithInMemoryAuthCredentials.zip")
    except (ServiceApiException, ServiceUsageException, SdkException):
        logging.exception("Exception encountered while executing operation")
