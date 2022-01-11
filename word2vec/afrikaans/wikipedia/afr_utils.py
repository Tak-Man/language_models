import json
import re
import pandas as pd
import os
import numpy as np
from tqdm import tqdm


def get_stop_words(json_file="./word2vec_af_wikipedia.json",
                   number_of_stop_words=None,
                   word_count_threshold=0.30,
                   remove_punctuation=True,
                   lowercase_words=True,
                   remove_proper_nouns=True):
    with open(json_file, "r") as read_file:
        data = json.load(read_file)
        token_counts = data["token_counts"]

    if remove_punctuation:
        token_counts = [(re.sub(r"[^a-zA-Z]", "", x), y) for x, y in token_counts if re.sub(r"[^a-zA-Z]", "", x) != ""]

    if lowercase_words:
        token_counts = [(x.lower(), y) for x, y in token_counts]

    if remove_proper_nouns:
        proper_nouns = ["January", "january", "Januarie", "januarie",
                        "February", "february", "Februarie", "februarie",
                        "March", "march", "Maart", "maart",
                        "April", "april", "April", "april",
                        "May", "may", "Mei", "mei",
                        "June", "june", "Junie", "junie",
                        "July", "july", "Julie", "julie",
                        "August", "august", "Augustus", "augustus",
                        "September", "september", "September", "september",
                        "October", "october", "Oktober", "oktober",
                        "November", "november", "November", "november",
                        "December", "december", "Desember", "desember"]

        token_counts = [(x, y) for x, y in token_counts if x not in proper_nouns]

    token_dict = {}
    for token, count in token_counts:
        if token in token_dict:
            token_dict[token] = token_dict[token] + count
        else:
            token_dict[token] = count

    tokens_sorted = sorted(token_dict.items(), key=lambda x: x[1], reverse=True)

    if not number_of_stop_words:
        count_total = sum(token_dict.values())
        # print("count_total :", count_total)
        threshold_count = count_total * word_count_threshold
        # print("threshold_count :", threshold_count)
        running_total = 0
        idx = 0
        for _, count in token_counts:
            running_total += count
            idx += 1
            if running_total > threshold_count:
                break

        return_tokens = [x for x, y in tokens_sorted]
        return_tokens = return_tokens[:idx]
    else:
        return_tokens = [x for x, y in tokens_sorted]
        return_tokens = return_tokens[:number_of_stop_words]

    return return_tokens


def convert_df_to_text(input_df, section_name):
    len_input = len(input_df)

    if len_input == 0:
        return "", 0
    else:
        if len(section_name) > 0:
            return_text = section_name
            # return_text += "\n"
        else:
            return_text = ""

        rows = input_df.values

        for row in rows:
            return_text += "\n"
            return_text += " ".join(row.tolist())

    return return_text, len(rows)


def create_question_words_file_from_excel(source_excel_file,
                                          words_file_dir="./",
                                          words_file_name="question-words-afrikaans.txt"):
    excel_data = pd.ExcelFile(source_excel_file)

    excluded_entries = [0, 0.0, "0", "#N/A", "", "nan"]
    target_columns = ["Afrikaans_1", "Afrikaans_2", "Afrikaans_3", "Afrikaans_4"]
    target_columns_alt = ["Afrikaans_1", "Afrikaans_2", "Afrikaans_5", "Afrikaans_6"]

    all_text = ""
    total_rows = 0

    for sheet_name in tqdm(excel_data.sheet_names, desc="Processing sheets"):
        nan_value = np.nan # float("NaN")

        # print("sheet_name :", sheet_name)
        # print(f">> Processing sheet-{sheet_name}")
        excel_data = pd.read_excel(source_excel_file, sheet_name)
        [excel_data.replace(x, nan_value, inplace=True) for x in excluded_entries]

        excel_data_alt = excel_data.loc[:, target_columns_alt]
        excel_data_alt.dropna(inplace=True)

        excel_data = excel_data[target_columns]
        excel_data.dropna(inplace=True)
        excel_data = excel_data.drop_duplicates()

        if len(excel_data_alt) > 0:
            excel_data_alt.columns = target_columns
            excel_data = pd.concat([excel_data, excel_data_alt], axis=0)

        excel_data = excel_data.sort_values(target_columns)
        # print("excel_data :")
        # print(excel_data.shape)

        excel_text, no_rows = convert_df_to_text(input_df=excel_data, section_name=": " + sheet_name)
        # print("excel_text: ")
        # print(excel_text)

        if len(excel_text) > 0:
            total_rows += no_rows
            if len(all_text) > 0:
                all_text += "\n"
                all_text += excel_text
            else:
                all_text = excel_text

    save_file_name = os.path.join(words_file_dir, words_file_name)
    # print("save_file_name :", save_file_name)
    with open(save_file_name, "w", encoding="utf8") as out_file: # utf8 latin1
        out_file.write(all_text)
        # out_file.write("Testing testing")

    return total_rows


