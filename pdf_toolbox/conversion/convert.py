import shutil
import utils.constants
import logging, sqlite3
import pandas as pd
from pathlib import Path

def convert_db_markdown(original_src, with_imgs=True):
    """Converts extracted content from database entries into markdown format."""
    original_src = Path(original_src).resolve()
    name = original_src.name
    new_name = name.replace("-", "_").replace(".", "_").replace("*", "_")
    query = f"SELECT `Element Type`, `Image Path`, `Table Path`, Text FROM {new_name};"
    con = sqlite3.connect(utils.constants.database)
    cursor = con.cursor()
    cursor.execute(query)
    query_tuples = cursor.fetchall()
    query_list = [list(row) for row in query_tuples]
    formatted = []
    if with_imgs == True:
        out = utils.constants.converted_dir / f"markdown/with-images/{new_name}/{new_name}.md"
    else:
        out = utils.constants.converted_dir / f"markdown/without-images/{new_name}/{new_name}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    for db_info in query_list:
        if db_info[-1] in utils.constants.unwanted_pdf:
            pass
        elif db_info[0] in utils.constants.headings:
            temp_list = db_info
            temp_list[-1] = "## " + db_info[-1] + "\n\n"
            formatted.append(temp_list)
        elif db_info[0] in utils.constants.lists:
            temp_list = db_info
            temp_list[-1] = "- " + db_info[-1] + "\n"
            formatted.append(temp_list)
        elif db_info[0] in utils.constants.paragraphs:
            formatted.append(db_info)
        elif db_info[0] in utils.constants.figures and str(db_info[2]).endswith(".csv"):
            temp_list = db_info
            img_path = db_info[1]
            csv_path = db_info[2]
            tab_path = Path(csv_path).with_suffix(".md")
            _convert_csv_md_tables(csv_path, tab_path)
            with open(tab_path, "r") as stream:
                tab_string = stream.read()
            temp_list[-1] = f"{tab_string}\n\n"
            formatted.append(temp_list)
        elif db_info[0] in utils.constants.figures and str(db_info[1]).endswith(".png") and with_imgs == True:
            temp_list = db_info
            path = Path(db_info[1]).resolve()
            img_dir = out.parent / "figures"
            img_out = Path(img_dir / path.name).resolve()
            img_dir.mkdir(parents=True, exist_ok=True)
            rel_path = "./" + "figures/" + path.name
            shutil.copy2(path, img_out)
            temp_list[-1] = f"![Image]({rel_path})\n\n"
            formatted.append(temp_list)
        elif db_info[0] in utils.constants.table_rows:
            pass
    final = formatted
    with open(out, "w") as stream:
        for item in final:
            cur_index = formatted.index(item)
            prev_index = cur_index - 1
            if prev_index < 0:
                stream.writelines(item[-1])
            elif formatted[prev_index][0] in utils.constants.lists and formatted[cur_index][0] in utils.constants.headings:
                stream.write("\n")
                stream.writelines(item[-1])
            elif formatted[prev_index][0] in utils.constants.paragraphs and formatted[cur_index][0] in utils.constants.headings:
                stream.write("\n\n")
                stream.writelines(item[-1])
            elif formatted[prev_index][0] in utils.constants.lists and formatted[cur_index][0] in utils.constants.figures:
                stream.write("\n")
                stream.writelines(item[-1])
            elif formatted[prev_index][0] in utils.constants.paragraphs and formatted[cur_index][0] in utils.constants.figures:
                stream.write("\n\n")
                stream.writelines(item[-1])
            elif formatted[prev_index][0] in utils.constants.lists and formatted[cur_index][0] in utils.constants.paragraphs:
                stream.write("\n")
                stream.writelines(item[-1])
            elif formatted[prev_index][0] in utils.constants.paragraphs and formatted[cur_index][0] in utils.constants.lists:
                stream.write("\n\n")
                stream.writelines(item[-1])
            else:
                stream.writelines(item[-1])


def _convert_csv_md_tables(csv_file, tab_path):
    """Converts found ".csv" tables into Github markdown formatting using Pandas."""
    df = pd.read_csv(csv_file, engine="python")
    with open(tab_path, "w") as stream:
        df.fillna("", inplace=True)
        df.to_markdown(buf=stream, tablefmt="github")
