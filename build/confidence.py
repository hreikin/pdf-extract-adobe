import logging

from pathlib import Path
from difflib import SequenceMatcher, get_close_matches

def confidence_check_text(input_path):
    """
    Recursively finds two pre-determined text files to be used for a very basic 
    confidence check.

    The confidence check uses the difflib "SequenceMatcher" class and 
    "get_close_matches()" method to compare two files created with the 
    "_iterate_through_nested_dicts()" and "ocr_converted_pdf_images()" functions 
    before returning a ratio. All ratios and averages are stored to a dictionary 
    and text file.

    The Python docs state that "ratio()" returns a float in [0, 1], measuring 
    the similarity of the sequences. As a rule of thumb, a "ratio()" value over 
    0.6 means the sequences are close matches. The same value of 0.6 is used as 
    the cut-off for the "get_close_matches()" method.

    :param input_path: Directory which contains the extracted/OCR text files.
    """
    input_path = Path(input_path)
    final_score_dict = dict()
    for directory in input_path.iterdir():
        if directory.is_dir():
            txt_file_list = sorted(directory.rglob("*.txt"))
            ocr_txt_file = txt_file_list[0]
            json_txt_file = txt_file_list[-1]
            logging.debug(f"Comparing '{ocr_txt_file.resolve()}' with '{json_txt_file.resolve()}'")
            with open(ocr_txt_file) as stream:
                ocr_list = stream.readlines()
            with open(json_txt_file) as stream:
                json_list = stream.readlines()
            close_matches_a = 0
            for line in ocr_list:
                matches_list = get_close_matches(line, json_list, n=1)
                if len(matches_list) > 0:
                    close_matches_a += 1
                matches_list = []
            close_match_ratio_a = close_matches_a / len(ocr_list)
            close_matches_b = 0
            for line in json_list:
                matches_list = get_close_matches(line, ocr_list, n=1)
                if len(matches_list) > 0:
                    close_matches_b += 1
                matches_list = []
            close_match_ratio_b = close_matches_b / len(json_list)
            with open(ocr_txt_file) as stream:
                ocr_string = stream.read()
            with open(json_txt_file) as stream:
                json_string = stream.read()
            reverse_ocr_string = ocr_string[::-1]
            reverse_json_string = json_string[::-1]
            score_a = SequenceMatcher(None, json_string, ocr_string)
            score_b = SequenceMatcher(None, ocr_string, json_string)
            score_c = SequenceMatcher(None, reverse_json_string, reverse_ocr_string)
            score_d = SequenceMatcher(None, reverse_ocr_string, reverse_json_string)
            comparison_ratio = (score_a.ratio() + score_b.ratio() + score_c.ratio() + score_d.ratio()) / 4
            close_match_average_ratio = (close_match_ratio_a + close_match_ratio_b) / 2
            total_average_ratio = (comparison_ratio + close_match_average_ratio) / 2
            logging.debug(f"Close Match Ratio A: '{close_match_ratio_a}'")
            logging.debug(f"Close Match Ratio B: '{close_match_ratio_b}'")
            logging.debug(f"Close Match Average Ratio: '{close_match_average_ratio}'")
            logging.debug(f"Comparison Ratio: '{comparison_ratio}'")
            logging.debug(f"Total Average Ratio: '{total_average_ratio}'")
            final_score_dict[directory.name.replace('-Extracted-Json-Schema', '')] = {
                "Comparison A Ratio" : score_a.ratio(),
                "Comparison B Ratio" : score_b.ratio(),
                "Comparison C Ratio" : score_c.ratio(),
                "Comparison D Ratio" : score_d.ratio(),
                "Comparison Average Ratio" : comparison_ratio,
                "Close Match Ratio A" : close_match_ratio_a,
                "Close Match Ratio B" : close_match_ratio_b,
                "Close Match Average Ratio" : close_match_average_ratio,
                "Total Average Ratio" : total_average_ratio,
            }
    output_file = "../test/all-confidence-scores.txt"
    logging.debug(f"Creating text output file with results '{Path(output_file).resolve()}'.")
    with open(output_file, "w") as stream:
        stream.write(f"PDF".ljust(50) + f"Score".rjust(30))
        for pdf, scores in final_score_dict.items():
            stream.write(f"\n{pdf}\n")
            for key, value in scores.items():
                stream.write(f"---- {key}:".ljust(50) + f"{round(value, 1)}\n".rjust(30))
