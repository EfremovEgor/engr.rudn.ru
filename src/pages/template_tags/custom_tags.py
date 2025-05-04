import enum
from django.template.defaulttags import register
from pages.utils import aliases, functions
from django.utils.translation import ngettext
from django import template
from django.utils.translation import gettext_lazy as _


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
def format_prices(profile_data: dict) -> list[str]:
    prices = [
        profile_data.get("price_first_year"),
        profile_data.get("price_second_year"),
        profile_data.get("price_third_year"),
        profile_data.get("price_fourth_year"),
        profile_data.get("price_fifth_year"),
    ]

    if prices[0] is None:
        return []

    max_year = int(profile_data.get("study_duration", 5))
    rows: list[str] = []

    for idx, price in enumerate(prices):
        if price is None:
            break

        year_num = idx + 1

        is_last = (
            year_num == 5                                        
            or year_num == max_year                        
            or (idx + 1 < len(prices) and prices[idx + 1] is None)
        )

        if is_last:
            rows.append(
                _("%(n)d‑й год и далее – %(p)s ₽")
                % {"n": year_num, "p": price}
            )
            break

        rows.append(
            _("%(n)d‑й год – %(p)s ₽")
            % {"n": year_num, "p": price}
        )

    return rows


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
def create_study_duration_badge_text(profile_data: dict) -> str:
    details = (
        profile_data.get("full_time_details")
        or profile_data.get("part_time_details")
        or profile_data.get("extramural_details")
    )
    if not details:
        return ""

    duration = int(details["study_duration"])

    return ngettext(
        "%(num)d year",
        "%(num)d years",
        duration
    ) % {"num": duration}

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
