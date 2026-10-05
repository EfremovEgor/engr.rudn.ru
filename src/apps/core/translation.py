from modeltranslation.translator import TranslationOptions


class BaseTranslationOptions(TranslationOptions):
    # Русская версия обязательна там, где поле обязательно; английская — всегда опциональна.
    required_languages = ("ru",)
