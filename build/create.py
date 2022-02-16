import constants
import logging, sqlite3
from pathlib import Path

def create_markdown(src_json_dir):
    src_json_dir = Path(src_json_dir).resolve()
    name = src_json_dir.name
    new_name = name.replace("-", "_").replace(".", "_")
    query = f"SELECT `Element ID`, `Element Type`, `Image Path`, `Table Path`, Text FROM {new_name};"
    con = sqlite3.connect(constants.database)
    cursor = con.cursor()
    cursor.execute(query)
    query_tuples = cursor.fetchall()
    query_list = [list(row) for row in query_tuples]
    formatted = []
    for db_info in query_list:
        if db_info[1] in constants.headings:
            temp_list = db_info
            temp_list[-1] = "## " + db_info[-1] + "\n\n"
            formatted.append(temp_list)
        elif db_info[1] in constants.lists:
            temp_list = db_info
            temp_list[-1] = "- " + db_info[-1] + "\n"
            formatted.append(temp_list)
        elif db_info[1] in constants.paragraphs:
            formatted.append(db_info)
        elif db_info[1] in constants.figures and str(db_info[3]).endswith(".csv"):
            temp_list = db_info
            img_path = db_info[2]
            csv_path = db_info[3]
            temp_list[-1] = f"![Table]({constants.src_dir}/json-schema/{name}/{csv_path})\n![Image]({constants.src_dir}/json-schema/{name}/{img_path})\n\n"
            formatted.append(temp_list)
        elif db_info[1] in constants.figures and str(db_info[2]).endswith(".png"):
            temp_list = db_info
            path = db_info[2]
            temp_list[-1] = f"![Image]({constants.src_dir}/json-schema/{name}/{path})\n\n"
            formatted.append(temp_list)
        elif db_info[1] in constants.table_rows:
            pass
    final = formatted
    out = constants.src_dir / f"converted/md/{new_name}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as stream:
        for item in final:
            cur_index = formatted.index(item)
            prev_index = cur_index - 1
            if formatted[cur_index][1] in constants.headings and prev_index < 0:
                stream.writelines(item[-1])
            elif formatted[prev_index][1] in constants.lists and formatted[cur_index][1] in constants.headings:
                stream.write("\n")
                stream.writelines(item[-1])
            elif formatted[prev_index][1] in constants.paragraphs and formatted[cur_index][1] in constants.headings:
                stream.write("\n\n")
                stream.writelines(item[-1])
            elif formatted[prev_index][1] in constants.lists and formatted[cur_index][1] in constants.figures:
                stream.write("\n")
                stream.writelines(item[-1])
            elif formatted[prev_index][1] in constants.paragraphs and formatted[cur_index][1] in constants.figures:
                stream.write("\n\n")
                stream.writelines(item[-1])
            elif formatted[prev_index][1] in constants.lists and formatted[cur_index][1] in constants.paragraphs:
                stream.write("\n")
                stream.writelines(item[-1])
            elif formatted[prev_index][1] in constants.paragraphs and formatted[cur_index][1] in constants.lists:
                stream.write("\n\n")
                stream.writelines(item[-1])
            else:
                stream.writelines(item[-1])
