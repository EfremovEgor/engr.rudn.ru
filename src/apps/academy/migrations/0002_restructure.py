# Переименование моделей и таблиц кафедр, адреса страниц кафедр в БД (вместо словаря в коде).
from django.db import migrations, models

from apps.core.migration_utils import immediate_constraints, move_content_type

# Бывший pages/utils/aliases.department_abbreviation_to_name
DEPARTMENT_SLUGS = {
    "КМПУ": "kmpu",
    "КМТ": "kmt",
    "КЭШ": "kesh",
    "КННД": "knnd",
    "КТТТ": "kttt",
    "КТСКМ": "ktskm",
    "КАРД": "kard",
    "КИМОП": "kimop",
    "КНМТ": "knmt",
    "КИЯ": "kiya",
    "КПАД": "kpad",
}


def fill_slugs(apps, schema_editor):
    Department = apps.get_model("academy", "Department")
    used = set()
    for department in Department.objects.order_by("position", "id"):
        slug = DEPARTMENT_SLUGS.get((department.abbreviation or "").strip().upper())
        if slug and slug not in used:
            used.add(slug)
            department.slug = slug
            department.save(update_fields=["slug"])


class Migration(migrations.Migration):

    dependencies = [
        ("academy", "0001_move_from_pages"),
        ("education", "0001_move_from_pages"),
        ("science", "0001_move_from_pages"),
        ("seminars", "0029_department_fk_to_academy"),
        ("pages", "0059_move_models_out"),
    ]

    operations = [
        move_content_type("academy", "departmentinfo", "academy", "department"),
        move_content_type("academy", "administrationprofiles", "academy", "administrationmember"),
        migrations.RenameModel("DepartmentInfo", "Department"),
        migrations.RenameModel("AdministrationProfiles", "AdministrationMember"),
        migrations.AlterModelTable("department", None),
        migrations.AlterModelTable("administrationmember", None),
        migrations.AddField(
            model_name="department",
            name="slug",
            field=models.SlugField(
                blank=True,
                help_text="Часть адреса: /academy/departments/<адрес>. Пусто — у кафедры нет отдельной страницы.",
                max_length=100,
                null=True,
                unique=True,
                verbose_name="Адрес страницы",
            ),
        ),
        immediate_constraints(),
        migrations.RunPython(fill_slugs, migrations.RunPython.noop),
    ]
