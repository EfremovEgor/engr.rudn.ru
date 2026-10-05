# Существующий контент (русская версия) переносится в поля *_ru переводов.
from django.db import migrations

from apps.core.migration_utils import copy_fields


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0060_translations_and_options"),
    ]

    operations = [
        copy_fields("pages", "IndexContact", {"sub_heading": "sub_heading_ru", "location": "location_ru", "heading": "heading_ru", "working_hours": "working_hours_ru"}),
        copy_fields("pages", "MainSlider", {"image_full": "image_full_ru", "image_mobile": "image_mobile_ru", "name": "name_ru"}),
    ]
