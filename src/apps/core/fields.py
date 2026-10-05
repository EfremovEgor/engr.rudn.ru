from django.db import models


class RichTextField(models.TextField):
    """HTML-контент, редактируемый в CKEditor 5 с загрузкой файлов в медиатеку.

    В миграциях поле сериализуется как обычный TextField: смена редактора
    никогда не требует миграций БД.
    """

    def formfield(self, **kwargs):
        from django_ckeditor_5.widgets import CKEditor5Widget

        kwargs.setdefault("widget", CKEditor5Widget(config_name="default"))
        return super().formfield(**kwargs)

    def deconstruct(self):
        name, _path, args, kwargs = super().deconstruct()
        return name, "django.db.models.TextField", args, kwargs
