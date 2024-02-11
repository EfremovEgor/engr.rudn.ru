import enum
from django.template.defaulttags import register
from pages.utils import aliases


@register.filter
def get_item(dictionary, key):
    print(dictionary)
    return dictionary.get(key)


@register.filter
def get_alias_lang(key):
    return aliases.lang_aliases.get(key.lower())


@register.filter
def study_level_to_page_name(key):
    return aliases.study_level_to_page_name.get(key.lower())


@register.filter
def replace_quotes(phrase):
    return "» /	«".join([part.strip() for part in phrase.split("/")])


@register.filter
def temp_replace_head_department(phrase: str):
    return phrase.replace("кафедры", "кафедрой")


@register.filter
def get_corresponding_scores(data: list, key: str):
    for record in data:
        if record["subject"] == key:
            return record["score"]
    return None


@register.filter
def format_scores(data: dict, subject_type: str):
    def find_subject_in_scores(scores, subject):
        for record in scores:
            if record["subject"] == subject:
                return record["score"]
        return None

    if data["minimal_passing_scores_budget"] is not None:
        strings = []
        for record in data["minimal_passing_scores_budget"][subject_type]:

            strings.append(
                f"{record['subject']} – {record['score']} ({find_subject_in_scores(data['minimal_passing_scores_budget'][subject_type],record['subject'])} для обучения по контракту)"
            )

        return strings
    strings = []
    for record in data["minimal_passing_scores_contract"][subject_type]:
        strings.append(f"{record['subject']} – {record['score']} (контракт)")
    return strings


@register.filter
def format_prices(data: dict):
    strings = []
    max_year = data["study_duration"]
    prices = [
        data["price_first_year"],
        data["price_second_year"],
        data["price_third_year"],
        data["price_fourth_year"],
        data["price_fifth_year"],
    ]
    for i, price in enumerate(prices):
        if i == 4 or i + 1 == max_year:
            strings.append(f"{i+1}-й год – {price} ₽")
            break
        if prices[i + 1] == None:
            strings.append(f"{i+1}-й год и далее – {price} ₽")
            break
        strings.append(f"{i+1}-й год – {price} ₽")

    return strings
