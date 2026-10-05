# Существующий контент (русская версия) переносится в поля *_ru переводов.
from django.db import migrations

from apps.core.migration_utils import copy_fields


class Migration(migrations.Migration):

    dependencies = [
        ("education", "0007_translations_and_options"),
    ]

    operations = [
        copy_fields("education", "AdditionalProgram", {"language": "language_ru", "volume": "volume_ru", "information": "information_ru", "title": "title_ru", "study_mode": "study_mode_ru", "description": "description_ru"}),
        copy_fields("education", "Program", {"content": "content_ru", "name": "name_ru"}),
        copy_fields("education", "ProgramOffer", {"note": "note_ru"}),
        copy_fields("education", "StudyDirection", {"name": "name_ru"}),
    ]
