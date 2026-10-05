# Существующий контент (русская версия) переносится в поля *_ru переводов.
from django.db import migrations

from apps.core.migration_utils import copy_fields


class Migration(migrations.Migration):

    dependencies = [
        ("science", "0003_translations_and_options"),
    ]

    operations = [
        copy_fields("science", "DissertationCommittee", {"faculty": "faculty_ru", "secretary": "secretary_ru", "address": "address_ru", "deputy": "deputy_ru", "chairman": "chairman_ru", "organization": "organization_ru", "composition": "composition_ru"}),
        copy_fields("science", "Equipment", {"name": "name_ru", "purpose": "purpose_ru"}),
        copy_fields("science", "Partner", {"about": "about_ru", "name": "name_ru", "result": "result_ru", "collaboration_direction": "collaboration_direction_ru"}),
        copy_fields("science", "ScientificCenter", {"field_name": "field_name_ru", "name": "name_ru", "content": "content_ru", "brief_description": "brief_description_ru"}),
        copy_fields("science", "ScientificSpecialty", {"name": "name_ru"}),
    ]
