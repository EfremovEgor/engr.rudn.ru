from django.template.defaulttags import register
from pages.utils import aliases


@register.filter
def get_item(dictionary, key):
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
