database = "../test/sqlite/pcc.sqlite"
headings = ["Title"]
paragraphs = ["P", "LBody", "ParagraphSpan", "Span", "StyleSpan"]
lists = ["L"]
table_rows = ["TR"]
figures = ["Figure", "Table"]
for i in range(0, 101):
    headings.append(f"H{i}")
    paragraphs.append(f"P[{i}]")
    lists.append(f"LI[{i}]")
    table_rows.append(f"TR[{i}]")
    figures.append(f"Table[{i}]")
    figures.append(f"Figure[{i}]")