# Python Content Creator
> PCC is in development so things will break regularly until a solid base for 
> the program has been created.

Python Content Creator (PCC) aims to be an all round content extraction, 
conversion and creation program. The goal is to extract content from various 
file formats and store it in a database for use in other document creation. 

This should hopefully allow easier conversion to other formats and also let you 
create new documents using any text, tables, pictures, etc you may already have 
available in other file formats.

## Install
- Place `Adobe PDF Extract API` credentials in root of repository.
- Install `Python Imaging Library` (or the `Pillow fork`) for your OS
- Install `Tesseract OCR` for your OS.
- Install `wxGTK-devel` for your OS (Linux only)

```
python3 -m venv .venv
source .venv/bin/activate
pip install scrapy pdfservices-sdk pytesseract pypdf2 pymupdf sqlitebiter wxwidgets pandas tabulate
```

## Known Issue & Workaround
On Linux (Windows/Mac untested) the file `.venv/lib64/python3.9/site-packages/ado
be/pdfservices/operation/internal/io/file_ref_impl.py` from `pdfservices-sdk` 
inside the `venv` you create needs a few changes otherwise it might fail with a 
false `cross-device link` error.

Add `import shutil` to the top of the file and on line 46 alter it to the 
following to successfully save the JsonSchema/zip file it outputs. This does not 
deal with deleting the temporary file as it only copies it however with it being 
in temp it should be deleted on a reboot anyway so for now this hacky workaround 
should be ok:

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
- [x] Create database with Json
- [ ] File conversion using info stored in database
