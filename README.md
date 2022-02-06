# PDF Content Extraction Using Adobe Extract API

## Install
- Place `Adobe PDF Extract API` credentials in root of repository.
- Install `Python Imaging Library` (or the `Pillow fork`) for your OS
- Install `Tesseract OCR` for your OS.

```
python3 -m venv .venv
source .venv/bin/activate
pip install scrapy pdfservices-sdk pytesseract pypdf2 pymupdf
```

## Known Issue & Workaround
On Linux (Windows/Mac untested) the file `.venv/lib64/python3.9/site-packages/ado
be/pdfservices/operation/internal/io/file_ref_impl.py` from `pdfservices-sdk` 
inside the `venv` you create needs a few changes otherwise it fails with a 
false `cross-device link` error.

Add `import shutil` to the top of the file and on line 46 alter it to the 
following to successfully save the JsonSchema/zip file it outputs :

```
shutil.copy(self._file_path, abs_path)
```

## Scores
The file `confidence.py` creates two text files for comparison to create a 
rudimentary confidence check as one isn't provided by the API. Scores are 
calculated using the `SequenceMatcher` class and `get_close_matches` method from 
`difflib`. 

A score of **0.6** for any of the calculated scores is considered a close match. 
All scores are stored in a dictionary and a text file is created with the 
results.

## TODO
- [x] Create broad function to target all required items
- [x] Display text only output using print or similar
- [x] Accuracy check of extracted Json
- [ ] Create database with Json
