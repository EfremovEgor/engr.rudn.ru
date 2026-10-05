# Вторая часть 0030: изменения схемы отдельно от изменения данных
# (PostgreSQL не позволяет менять схему таблицы с отложенными проверками FK в той же транзакции).
import django.db.models.deletion
from django.db import migrations, models

from apps.core.migration_utils import immediate_constraints


def fill_positions(apps, schema_editor):
    Seminar = apps.get_model("seminars", "Seminar")
    Seminar.objects.filter(position=None).update(position=0)


class Migration(migrations.Migration):

    dependencies = [
        ("seminars", "0030_restructure"),
    ]

    operations = [
        migrations.RemoveField(model_name="seminar", name="reports"),
        migrations.AlterField(
            model_name="seminarreport",
            name="seminar",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reports",
                to="seminars.seminar",
                verbose_name="Семинар",
            ),
        ),
        migrations.RenameField("seminar", "chair1", "chair"),
        migrations.RenameField("seminar", "organizer1", "organizer"),
        immediate_constraints(),
        migrations.RunPython(fill_positions, migrations.RunPython.noop),
    ]
