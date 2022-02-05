# PDF Content Extraction Using Adobe Extract API

## Folder Contents
This contains example output from the Adobe Extract API. All files within this 
directory (except the `structuredData-pretty.json` file) are examples of what is 
inside the ZIP file returned from the API.

### Figures
Contains `.png` format images that were found within the PDF and extracted.

### Tables
Contains `.png` format image and `.csv` format pairs of any table data that was 
found within the PDF.

### Structured Data
The `structuredData.json` file contains the extracted content & PDF element 
structure. See [JSON Schema](https://developer.adobe.com/document-services/docs/b9e0ca07f1e92db6453016fff44a8c31/extractJSONOutputSchema2.json) for a description of the default output.