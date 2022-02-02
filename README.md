# PDF Content Extraction Using Adobe Extract API

## Install
- Place `Adobe PDF Extract API` credentials in root of repository.
- Install `Tesseract OCR` for your OS.

```
python3 -m venv .venv
source .venv/bin/activate
pip install scrapy pdfservices-sdk pdf2image pytesseract
```

## Known Issue & Workaround
On Linux (Windows/Mac untested) the file `.venv/lib64/python3.9/site-packages/ado
be/pdfservices/operation/internal/io/file_ref_impl.py` from `pdfservices-sdk` 
inside the `venv` you create needs `import shutil` adding to the top of 
the file and line 46 altering to the following to successfully save the 
JsonSchema/zip file it outputs:

```
shutil.copy(self._file_path, abs_path)
```

## TODO
- [x] Create broad function to target all required items
- [x] Display text only output using print or similar
- [ ] Accuracy check of extracted Json
- [ ] Create database with Json
