# Модели переехали в приложения academy, education и science (см. их 0001_move_from_pages).
# Удаляем их только из состояния Django — таблицы и данные остаются.
from django.db import migrations

MOVED = [
    "StudyDirection",
    "Profile",
    "ProfileDetails",
    "AdditionalEducationItem",
    "AdditionalEducation",
    "AdministrationProfiles",
    "ScientificCenters",
    "DissertationCommittee",
    "ScientificSpecialty",
    "EquipmentData",
    "PartnerData",
    "DepartmentInfo",
]


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0058_additionaleducationitem_description"),
        ("academy", "0001_move_from_pages"),
        ("education", "0001_move_from_pages"),
        ("science", "0001_move_from_pages"),
        ("seminars", "0029_department_fk_to_academy"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[migrations.DeleteModel(name=name) for name in MOVED],
            database_operations=[],
        ),
    ]
