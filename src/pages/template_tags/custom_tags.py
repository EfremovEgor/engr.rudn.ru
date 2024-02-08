from django.template.defaulttags import register
from pages.utils import aliases


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_alias_lang(key):
    return aliases.lang_aliases.get(key.lower())
