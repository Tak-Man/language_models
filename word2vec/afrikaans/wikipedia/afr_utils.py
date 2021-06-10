import json
import re


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


if __name__ == "__main__":
    stop_words = get_stop_words(json_file="./word2vec_af_wikipedia.json",
                                number_of_stop_words=None,
                                word_count_threshold=0.30,
                                remove_punctuation=True,
                                lowercase_words=True)

    print("stop_words :", stop_words)
    print("len(stop_words) :", len(stop_words))

