from pathlib import Path

# This is the only variable to be changed from elsewhere. All the rest should 
# remain constant.
cur_file = Path()

base_dir = Path("..").resolve()
src_dir = base_dir / "src"
confidence_dir = src_dir / "confidence"
converted_dir = src_dir / "converted"
created_dir = src_dir / "created"
extracted_dir = src_dir / "extracted"
json_dir = src_dir / "json"
pdf_dir = src_dir / "pdfs"
zip_dir = src_dir / "zips"
database = src_dir / "sqlite" / "pcc.sqlite"
headings = []
paragraphs = ["P", "LBody", "ParagraphSpan", "Span", "StyleSpan"]
lists = ["L"]
table_rows = ["TR"]
figures = ["Figure", "Table"]
unwanted_pdf = ["*", "◈", "-", "•", "* ", "◈ ", "- ", "• ", ":", ": ", ".    "]
# Append more headings.
for i in range(0, 201):
    headings.append(f"H{i}")
    paragraphs.append(f"P[{i}]")
    lists.append(f"LI[{i}]")
    table_rows.append(f"TR[{i}]")
    figures.append(f"Table[{i}]")
    figures.append(f"Figure[{i}]")
