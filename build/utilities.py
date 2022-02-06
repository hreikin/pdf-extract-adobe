import zipfile, logging

from pathlib import Path

def extract_from_zip(zip_source):
    """
    Recursively finds all zip files within a source directory and un-zips them to 
    a given output directory.

    :param zip_source: A directory containing zip files.
    :param output_path: The directory to extract the zip contents in to.
    """
    # Extracts Json Schema from zip file.
    output_path = Path(zip_source).with_stem("json-schema")
    Path(output_path).mkdir(parents=True, exist_ok=True)
    zip_file_list = sorted(Path(zip_source).rglob("*.zip"))
    zip_amount = len(zip_file_list)
    logging.info(f"Found {zip_amount} zip files, extracting to '{Path(output_path).resolve()}'.")
    for zip_file in zip_file_list:
        dir_name = zip_file.stem
        with zipfile.ZipFile(zip_file) as item:
            item.extractall(output_path / dir_name)
        logging.debug(f"Extracted '{Path(zip_file).resolve()}'.")