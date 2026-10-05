# Существующий контент (русская версия) переносится в поля *_ru переводов.
from django.db import migrations

from apps.core.migration_utils import copy_fields


class Migration(migrations.Migration):

    dependencies = [
        ("seminars", "0031_translations_and_options"),
    ]

    operations = [
        copy_fields("seminars", "Seminar", {"description": "description_ru", "name": "name_ru"}),
        copy_fields("seminars", "SeminarReport", {"annotation": "annotation_ru", "name": "name_ru"}),
        copy_fields("seminars", "SeminarSpeaker", {"middle_name": "middle_name_ru", "bio": "bio_ru", "job_title": "job_title_ru", "first_name": "first_name_ru", "last_name": "last_name_ru", "academic_degree": "academic_degree_ru", "academic_title": "academic_title_ru"}),
    ]
