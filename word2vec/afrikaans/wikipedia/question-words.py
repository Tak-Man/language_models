import afr_utils as utils


if __name__ == "__main__":
    # Test create_question_words_file_from_excel()
    # ------------------------------------------------------------------------------------------------------
    source_excel_file = "../../../../../Full_Metal_Bitch_Data/retrieve-website-links/tests/question-words.xlsx"
    words_file_dir = "../../../../../Full_Metal_Bitch_Data/retrieve-website-links/tests/" # "./"
    words_file_name = "questions-words-afrikaans.txt"
    len_all_text = utils.create_question_words_file_from_excel(source_excel_file=source_excel_file,
                                                               words_file_dir=words_file_dir,
                                                               words_file_name=words_file_name)
    print("Question Words file written ({:,} lines)".format(len_all_text))
    # ------------------------------------------------------------------------------------------------------