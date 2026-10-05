# Понятные имена моделей и таблиц образовательного сервиса.
from django.db import migrations

from apps.core.migration_utils import move_content_type


class Migration(migrations.Migration):

    dependencies = [
        ("education", "0005_normalize_codes"),
    ]

    operations = [
        move_content_type("education", "profile", "education", "program"),
        move_content_type("education", "profiledetails", "education", "programoffer"),
        move_content_type("education", "additionaleducation", "education", "translatormodule"),
        move_content_type("education", "additionaleducationitem", "education", "additionalprogram"),
        migrations.RenameModel("Profile", "Program"),
        migrations.RenameModel("ProfileDetails", "ProgramOffer"),
        migrations.RenameModel("AdditionalEducation", "TranslatorModule"),
        migrations.RenameModel("AdditionalEducationItem", "AdditionalProgram"),
        migrations.RenameField("program", "faculty_field", "department"),
        migrations.RenameField("program", "language_fields", "languages"),
        migrations.AlterModelTable("studydirection", None),
        migrations.AlterModelTable("program", None),
        migrations.AlterModelTable("programoffer", None),
        migrations.AlterModelTable("translatormodule", None),
        migrations.AlterModelTable("additionalprogram", None),
    ]
