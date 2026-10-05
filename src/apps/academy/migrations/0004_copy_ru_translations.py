# Существующий контент (русская версия) переносится в поля *_ru переводов.
from django.db import migrations

from apps.core.migration_utils import copy_fields


class Migration(migrations.Migration):

    dependencies = [
        ("academy", "0003_translations_and_options"),
    ]

    operations = [
        copy_fields("academy", "Department", {"info": "info_ru", "name": "name_ru"}),
    ]
