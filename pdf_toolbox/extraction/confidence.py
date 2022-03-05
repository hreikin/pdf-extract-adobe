import logging
import utilities.constants

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
            ocr_txt_file = txt_file_list[0].resolve()
            json_txt_file = txt_file_list[1].resolve()
            pymupdf_txt_file = txt_file_list[2].resolve()
            logging.debug(f"Comparing '{ocr_txt_file.name}', '{json_txt_file.name}', '{pymupdf_txt_file.name}' and creating score.")
            ####################################################################
            # Close Match Scores                                               #
            ####################################################################
            with open(ocr_txt_file) as stream:
                ocr_list = stream.readlines()
            with open(json_txt_file) as stream:
                json_list = stream.readlines()
            with open(pymupdf_txt_file) as stream:
                pymupdf_list = stream.readlines()
            close_matches_a_ocr = 0
            for line in ocr_list:
                matches_list = get_close_matches(line, json_list, n=1)
                if len(matches_list) > 0:
                    close_matches_a_ocr += 1
                matches_list = []
            try:
                close_match_ratio_a_ocr = close_matches_a_ocr / len(ocr_list)
            except ZeroDivisionError:
                close_match_ratio_a_ocr = 0
            close_matches_b_ocr = 0
            for line in ocr_list:
                matches_list = get_close_matches(line, pymupdf_list, n=1)
                if len(matches_list) > 0:
                    close_matches_b_ocr += 1
                matches_list = []
            try:
                close_match_ratio_b_ocr = close_matches_b_ocr / len(ocr_list)
            except ZeroDivisionError:
                close_match_ratio_b_ocr = 0

            close_matches_a_json = 0
            for line in json_list:
                matches_list = get_close_matches(line, ocr_list, n=1)
                if len(matches_list) > 0:
                    close_matches_a_json += 1
                matches_list = []
            try:
                close_match_ratio_a_json = close_matches_a_json / len(json_list)
            except ZeroDivisionError:
                close_match_ratio_a_json = 0
            close_matches_b_json = 0
            for line in json_list:
                matches_list = get_close_matches(line, pymupdf_list, n=1)
                if len(matches_list) > 0:
                    close_matches_b_json += 1
                matches_list = []
            try:
                close_match_ratio_b_json = close_matches_b_json / len(json_list)
            except ZeroDivisionError:
                close_match_ratio_b_json = 0

            close_matches_a_pymupdf = 0
            for line in pymupdf_list:
                matches_list = get_close_matches(line, json_list, n=1)
                if len(matches_list) > 0:
                    close_matches_a_pymupdf += 1
                matches_list = []
            try:
                close_match_ratio_a_pymupdf = close_matches_a_pymupdf / len(pymupdf_list)
            except ZeroDivisionError:
                close_match_ratio_a_pymupdf = 0
            close_matches_b_pymupdf = 0
            for line in pymupdf_list:
                matches_list = get_close_matches(line, ocr_list, n=1)
                if len(matches_list) > 0:
                    close_matches_b_pymupdf += 1
                matches_list = []
            try:
                close_match_ratio_b_pymupdf = close_matches_b_pymupdf / len(pymupdf_list)
            except ZeroDivisionError:
                close_match_ratio_b_pymupdf = 0
            ####################################################################
            # Comparison Scores                                                #
            ####################################################################
            with open(ocr_txt_file) as stream:
                ocr_string = stream.read()
            with open(json_txt_file) as stream:
                json_string = stream.read()
            with open(pymupdf_txt_file) as stream:
                pymupdf_string = stream.read()
            reverse_ocr_string = ocr_string[::-1]
            reverse_json_string = json_string[::-1]
            reverse_pymupdf_string = pymupdf_string[::-1]
            score_a = SequenceMatcher(None, json_string, ocr_string)
            score_b = SequenceMatcher(None, json_string, pymupdf_string)
            score_c = SequenceMatcher(None, ocr_string, json_string)
            score_d = SequenceMatcher(None, ocr_string, pymupdf_string)
            score_e = SequenceMatcher(None, pymupdf_string, json_string)
            score_f = SequenceMatcher(None, pymupdf_string, ocr_string)
            score_g = SequenceMatcher(None, reverse_json_string, reverse_ocr_string)
            score_h = SequenceMatcher(None, reverse_json_string, reverse_pymupdf_string)
            score_i = SequenceMatcher(None, reverse_ocr_string, reverse_json_string)
            score_j = SequenceMatcher(None, reverse_ocr_string, reverse_pymupdf_string)
            score_k = SequenceMatcher(None, reverse_pymupdf_string, reverse_json_string)
            score_l = SequenceMatcher(None, reverse_pymupdf_string, reverse_ocr_string)
            ####################################################################
            # Averages & Totals                                                #
            ####################################################################
            close_match_average_ratio = (close_match_ratio_a_ocr + close_match_ratio_b_ocr + close_match_ratio_a_json + close_match_ratio_b_json + close_match_ratio_a_pymupdf + close_match_ratio_b_pymupdf) / 6
            comparison_ratio = (score_a.ratio() + score_b.ratio() + score_c.ratio() + score_d.ratio() + score_e.ratio() + score_f.ratio() + score_g.ratio() + score_h.ratio() + score_i.ratio() + score_j.ratio() + score_k.ratio() + score_l.ratio()) / 12
            total_average_ratio = (close_match_average_ratio + comparison_ratio) / 2
            logging.debug(f"Close Match Average Ratio: '{close_match_average_ratio}'")
            logging.debug(f"Comparison Ratio: '{comparison_ratio}'")
            logging.debug(f"Total Average Ratio: '{total_average_ratio}'")
            final_score_dict[directory.name] = {
                "Close Match OCR A" : close_match_ratio_a_ocr,
                "Close Match OCR B" : close_match_ratio_b_ocr,
                "Close Match JSON A" : close_match_ratio_a_json,
                "Close Match JSON B" : close_match_ratio_b_json,
                "Close Match PYMUPDF A" : close_match_ratio_a_pymupdf,
                "Close Match PYMUPDF B" : close_match_ratio_a_pymupdf,
                "Close Match Average Ratio" : close_match_average_ratio,
                "Comparison A" : score_a.ratio(),
                "Comparison B" : score_b.ratio(),
                "Comparison C" : score_c.ratio(),
                "Comparison D" : score_d.ratio(),
                "Comparison E" : score_e.ratio(),
                "Comparison F" : score_f.ratio(),
                "Comparison G" : score_g.ratio(),
                "Comparison H" : score_h.ratio(),
                "Comparison I" : score_i.ratio(),
                "Comparison J" : score_j.ratio(),
                "Comparison K" : score_k.ratio(),
                "Comparison L" : score_l.ratio(),
                "Comparison Average Ratio" : comparison_ratio,
                "Total Average Ratio" : total_average_ratio,
            }
    output_file = Path(f"{utilities.constants.confidence_dir}/all-confidence-scores.txt").resolve()
    logging.debug(f"Creating text output file with results '{output_file}'.")
    with open(output_file, "w") as stream:
        stream.write(f"PDF".ljust(50) + f"Score".rjust(30))
        for pdf, scores in final_score_dict.items():
            stream.write(f"\n{pdf}\n")
            for key, value in scores.items():
                stream.write(f"---- {key}:".ljust(50) + f"{round(value, 1)}\n".rjust(30))
