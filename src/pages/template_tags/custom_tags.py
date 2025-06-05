import enum
from django.template.defaulttags import register
from pages.utils import aliases, functions
from django.utils.translation import ngettext
from django import template
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language, get_language_info

RU_LABELS = {
    "ru": "Русский",
    "en": "Английский",
}

CANON = {
    "ru": "ru", "рус": "ru", "русский": "ru", "russian": "ru",
    "en": "en", "анг": "en", "английский": "en", "english": "en",
}

_LEVEL_CANON = {
    "bachelor": "bachelor",
    "bachelors": "bachelor",
    "бакалавриат": "bachelor",
    "бакалавриаты": "bachelor",

    "specialist": "specialist",
    "specialists": "specialist",
    "specialitet": "specialist",
    "speciality": "specialist",
    "специалитет": "specialist",
    "специалитеты": "specialist",

    "master": "master",
    "masters": "master",
    "магистратура": "master",
    "магистратуры": "master",

    "phd": "phd",
    "postgraduate": "phd",
    "postgraduates": "phd",
    "aspirantura": "phd",
    "aspirant": "phd",
    "aspirants": "phd",
    "аспирантура": "phd",
    "аспирантуры": "phd",
}

_TO_CODE = {
    "ru": "ru", "рус": "ru", "русский": "ru", "russian": "ru",
    "en": "en", "англ": "en", "английский": "en", "english": "en",
}

_RU_LOC = {
    "ru": "русском",
    "en": "английском",
}

_EN_NAME = {
    "ru": "Russian",
    "en": "English",
}

_RU_LEVEL = {
    "bachelor": "Бакалавриат",
    "specialist": "Специалитет",
    "master": "Магистратура",
    "phd": "Аспирантура",
}

_EN_LEVEL = {
    "bachelor": "Bachelor",
    "specialist": "Specialist",
    "master": "Master",
    "phd": "PhD",
}

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

    duration = details["study_duration"] 
    return f"{format_duration(duration)} {get_duration_suffix(duration)}"


@register.filter
def create_heading_with_duration(data: dict, details_type: str) -> str:
    block = data.get(details_type)
    if not block:
        return ""

    dur = block["study_duration"]
    return f"({format_duration(dur)} {get_duration_suffix(dur)})"


@register.filter
def slugify_url(string: str):
    return functions.make_slug(string)


@register.filter
def get_server_uri(_):
    return "https://academy.rudn.ru"


@register.filter
def truncate_url(url: str):
    return url[:-1] if url[-1] == "/" else url

@register.filter
def lang_code_to_label(raw_value: str) -> str:
    if not raw_value:
        return ""

    code = CANON.get(raw_value.lower(), raw_value.lower())

    ui_lang = (get_language() or "en")[:2]

    if ui_lang == "ru":
        return RU_LABELS.get(code, raw_value)

    try:
        return get_language_info(code)["name"]
    except KeyError:
        return raw_value

@register.filter
def langs_phrase(raw_list) -> str:
    if not raw_list:
        return ""

    codes = [_TO_CODE.get(str(x).lower(), str(x).lower()) for x in raw_list[:2]]

    ui = (get_language() or "en")[:2]

    if ui == "ru":
        if len(codes) == 2:
            return f"(на {_RU_LOC.get(codes[0])} и {_RU_LOC.get(codes[1])} языках)"
        return f"(на {_RU_LOC.get(codes[0])} языке)"

    if len(codes) == 2:
        return f"(in {_EN_NAME.get(codes[0])} and {_EN_NAME.get(codes[1])} languages)"
    return f"(in {_EN_NAME.get(codes[0])} language)"



@register.filter
def level_slug_to_label(raw: str) -> str:
    if not raw:
        return ""

    slug = _LEVEL_CANON.get(str(raw).strip().lower(), str(raw).strip().lower())
    ui = (get_language() or "en")[:2]

    if ui == "ru":
        return _RU_LEVEL.get(slug, raw)
    return _EN_LEVEL.get(slug, slug.capitalize())