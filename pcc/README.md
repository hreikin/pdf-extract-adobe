# PDF Content Extraction Using Adobe Extract API

## Folder Contents
This folder contains the scrapy spider and related files along with the python 
scripts for extraction, OCR, comparison, etc.

### Download
The `download` folder contains the majority of the scrapy spider files. The 
spider will first scrape the defined URL before finding and following all links 
it encounters. Any links with the `.pdf` extension are passed to the files 
pipeline for download in the `src` folder.

### Python Files
The file `extraction.py` focuses on communicating with the Adobe Extract API and 
extracting the downloaded ZIP files.

The file `confidence.py` creates two text files for comparison to create a 
rudimentary confidence check as one isn't provided by the API. Scores are 
calculated using the `SequenceMatcher` class and `get_close_matches` method from 
`difflib`. 

A score of **0.6** for any of the calculated scores is considered a close match. 
All scores are stored in a dictionary and a text file is created with the 
results.

The file `main.py` should be used to run the project. At the moment it simply 
calls all the relevant functions with the correct arguments provided in the 
order required.