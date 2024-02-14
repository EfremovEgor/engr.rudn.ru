import enum
from django.template.defaulttags import register
from pages.utils import aliases, functions


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

            string = f"{record['subject']} – {record['score']}"
            if record["score"] != find_subject_in_scores(
                data["minimal_passing_scores_contract"][subject_type], record["subject"]
            ):
                string += f" ({find_subject_in_scores(data['minimal_passing_scores_contract'][subject_type],record['subject'])} – на контракт)"
            strings.append(string)

        return strings
    strings = []
    for record in data["minimal_passing_scores_contract"][subject_type]:
        strings.append(f"{record['subject']} – {record['score']}")
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


@register.filter
def get_url_department_abbreviation(name: str):
    for k, v in aliases.department_abbreviation_to_name.items():
        if v == name:
            return k


def get_duration_suffix(duration: float):
    if duration in [2, 3, 4]:
        suffix = "года"
    if duration == 1:
        suffix = "год"
    if duration > 4:
        suffix = "лет"
    return suffix


@register.filter
def create_study_duration_badge_text(data: dict):
    string = "312"
    details = data["full_time_details"]
    if details is None:
        details = data["part_time_details"]
    if details is None:
        details = data["extramural_details"]
    suffix = get_duration_suffix(details["study_duration"])
    string = f"{details['study_duration']} {suffix}"
    return string


@register.filter
def create_heading_with_duration(data: dict, details_type: str):
    if details_type == "part_time_details":
        if data["full_time_details"] is not None:
            return f"({data['part_time_details']['study_duration']} {get_duration_suffix(data['part_time_details']['study_duration'])})"

    if details_type == "extramural_details":
        if (
            data["full_time_details"] is not None
            or data["part_time_details"] is not None
        ):
            return f"({data['extramural_details']['study_duration']} {get_duration_suffix(data['extramural_details']['study_duration'])})"

    return ""


@register.filter
def slugify_url(string: str):
    return functions.make_slug(string)


@register.filter
def get_server_uri(_):
    return "https://academy.rudn.ru"


@register.filter
def truncate_url(url: str):
    return url[:-1] if url[-1] == "/" else url
