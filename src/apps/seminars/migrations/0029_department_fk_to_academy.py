# Модель кафедры переехала из pages в academy: меняем ссылку только в состоянии Django.
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("seminars", "0028_seminarreport_video"),
        ("academy", "0001_move_from_pages"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name="seminar",
                    name="department",
                    field=models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="department_seminar",
                        to="academy.departmentinfo",
                        verbose_name="Департамент",
                    ),
                ),
            ],
            database_operations=[],
        ),
    ]
