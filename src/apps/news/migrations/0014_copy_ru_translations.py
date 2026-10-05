# Существующий контент (русская версия) переносится в поля *_ru переводов.
from django.db import migrations

from apps.core.migration_utils import copy_fields


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0013_translations_and_options"),
    ]

    operations = [
        copy_fields("news", "NewsItem", {"content": "content_ru", "title": "title_ru"}),
    ]
