# Четыре одинаковые модели документов объединены в одну Document с полем «Раздел».
import django.utils.timezone
from django.db import migrations, models

from apps.core.migration_utils import immediate_constraints

SOURCES = [
    ("ApplicantsCISNormativeDocument", "applicants_cis"),
    ("ApplicantsForeignNormativeDocument", "applicants_foreign"),
    ("OpenDaysFiles", None),
    ("StudentsApplications", "student_application"),
]
OPEN_DAYS_CATEGORY = {
    "Презентация": "open_days_presentation",
    "Фотография": "open_days_photo",
}


def copy_documents(apps, schema_editor):
    Document = apps.get_model("documents", "Document")
    created = []
    for model_name, category in SOURCES:
        model = apps.get_model("documents", model_name)
        ordering = ["position", "name", "id"] if model_name == "StudentsApplications" else ["name", "id"]
        for index, old in enumerate(model.objects.order_by(*ordering)):
            target_category = category or OPEN_DAYS_CATEGORY.get(old.type, "open_days_presentation")
            created.append(
                Document(
                    category=target_category,
                    name=old.name,
                    name_ru=old.name,
                    name_en=old.name_en,
                    file=old.file.name,
                    file_ru=old.file.name,
                    position=getattr(old, "position", index) if model_name == "StudentsApplications" else index,
                    is_published=True,
                )
            )
    Document.objects.bulk_create(created)


def remove_stale_content_types(apps, schema_editor):
    ContentType = apps.get_model("contenttypes", "ContentType")
    ContentType.objects.filter(
        app_label="documents", model__in=[name.lower() for name, _ in SOURCES]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("documents", "0007_applicantscisnormativedocument_name_en_and_more"),
        ("contenttypes", "0002_remove_content_type_name"),
        ("admin", "0003_logentry_add_action_flag_choices"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Document",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "is_published",
                    models.BooleanField(
                        db_index=True,
                        default=True,
                        help_text="Снимите галочку, чтобы скрыть материал на сайте, не удаляя его.",
                        verbose_name="Опубликовано",
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("applicants_cis", "Абитуриентам: нормативные документы (РФ и СНГ)"),
                            ("applicants_foreign", "Абитуриентам: нормативные документы (иностранные граждане)"),
                            ("open_days_presentation", "Дни открытых дверей: презентации"),
                            ("open_days_photo", "Дни открытых дверей: фотографии"),
                            ("student_application", "Студентам: образцы заявлений"),
                        ],
                        db_index=True,
                        max_length=64,
                        verbose_name="Раздел",
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Название")),
                ("name_ru", models.CharField(max_length=255, null=True, verbose_name="Название [ru]")),
                ("name_en", models.CharField(blank=True, max_length=255, null=True, verbose_name="Название [en]")),
                ("file", models.FileField(max_length=255, upload_to="documents", verbose_name="Файл")),
                ("file_ru", models.FileField(max_length=255, null=True, upload_to="documents", verbose_name="Файл [ru]")),
                ("file_en", models.FileField(blank=True, max_length=255, null=True, upload_to="documents", verbose_name="Файл [en]")),
                ("position", models.IntegerField(default=0, verbose_name="Позиция")),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True, verbose_name="Добавлен")),
            ],
            options={
                "verbose_name": "Документ",
                "verbose_name_plural": "Документы",
                "ordering": ["category", "position", "name"],
            },
        ),
        immediate_constraints(),
        migrations.RunPython(copy_documents, migrations.RunPython.noop),
        migrations.DeleteModel(name="ApplicantsCISNormativeDocument"),
        migrations.DeleteModel(name="ApplicantsForeignNormativeDocument"),
        migrations.DeleteModel(name="OpenDaysFiles"),
        migrations.DeleteModel(name="StudentsApplications"),
        immediate_constraints(),
        migrations.RunPython(remove_stale_content_types, migrations.RunPython.noop),
    ]
