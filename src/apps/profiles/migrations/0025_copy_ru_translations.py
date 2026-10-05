# Существующий контент (русская версия) переносится в поля *_ru переводов.
from django.db import migrations

from apps.core.migration_utils import copy_fields


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0024_translations_and_options"),
    ]

    operations = [
        copy_fields("profiles", "DepartmentStaff", {"department_responsibilities": "department_responsibilities_ru", "department_office": "department_office_ru"}),
        copy_fields("profiles", "EmployeeProfile", {"full_name": "full_name_ru", "content": "content_ru", "working_hours": "working_hours_ru", "job_title": "job_title_ru", "office": "office_ru"}),
        copy_fields("profiles", "StudentCommitteeProfile", {"full_name": "full_name_ru", "job_title": "job_title_ru", "office": "office_ru"}),
    ]
