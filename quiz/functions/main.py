from django.utils.translation.trans_real import translation
import yaml
import random
from datetime import datetime


def importFile(filename):
    with open(filename, "r", encoding="utf8") as file:
        yaml_data = yaml.safe_load(file)
    words = yaml_data["words"]
    return words


try:
    filename = "quiz/functions/db.yaml"
    words = importFile(filename)
except FileNotFoundError:
    filename = "db.yaml"
    words = importFile(filename)


def filter(selected_date):  # Expected "2024-09-05"
    if not selected_date == "":
        selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()

        quiz_words_list = []
        for i in range(len(words)):
            if words[i]["date"] == selected_date:
                quiz_words_list.append(words[i])
    else:
        quiz_words_list = words
    return quiz_words_list


def return_all_values(quiz_words_list):
    lexicon = []
    for i in range(len(quiz_words_list)):
        lexicon.append(quiz_words_list[i]["translations"])
    return lexicon


def count_words():
    count = len(list(words))
    return count


def quiz(difficulty_level, quiz_words_list):
    # The word to find
    the_word = random.choice(quiz_words_list)
    the_word = the_word["translations"]

    possible_answers_list = []

    if difficulty_level > 0:
        possible_answers_list.append(the_word["de"])
        while len(possible_answers_list) < difficulty_level:
            possible_answer = quiz_words_list[
                random.randint(0, len(quiz_words_list) - 1)
            ]["translations"]["de"]

            if possible_answer not in possible_answers_list:
                possible_answers_list.append(possible_answer)
        random.shuffle(possible_answers_list)

    return the_word, possible_answers_list


def find_the_correct(the_word, answer):
    if the_word["de"] == answer:
        return True
    else:
        return False


# filtered_words = filter("2024-09-05")
# all_val = return_all_values(filtered_words)


# the_word, possible_answers_list = quiz(3, filter("2024-09-05"))

print("")
