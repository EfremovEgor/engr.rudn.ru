# Доклад принадлежит одному семинару (FK вместо many-to-many) — доклады редактируются внутри семинара.
# Исправлены опасные каскады: удаление сотрудника/докладчика больше не удаляет семинары и доклады.
import uuid

import django.db.models.deletion
from django.db import migrations, models

from apps.core.migration_utils import immediate_constraints


def m2m_to_fk(apps, schema_editor):
    Seminar = apps.get_model("seminars", "Seminar")
    SeminarReport = apps.get_model("seminars", "SeminarReport")
    Through = Seminar.reports.through
    owner = {}
    for row in Through.objects.order_by("id"):
        if row.seminarreport_id not in owner:
            owner[row.seminarreport_id] = row.seminar_id
            SeminarReport.objects.filter(pk=row.seminarreport_id).update(seminar_id=row.seminar_id)
            continue
        if owner[row.seminarreport_id] == row.seminar_id:
            continue
        # Доклад был показан в нескольких семинарах — создаём копию для каждого следующего.
        report = SeminarReport.objects.get(pk=row.seminarreport_id)
        report.pk = None
        report.id = None
        report._state.adding = True
        report.uuid = uuid.uuid4()
        report.seminar_id = row.seminar_id
        report.save()
        print(f"\n  ! доклад #{row.seminarreport_id} был в нескольких семинарах; для семинара #{row.seminar_id} создана копия #{report.pk}")
    orphans = SeminarReport.objects.filter(seminar_id=None).count()
    if orphans:
        print(f"\n  ! {orphans} докладов не привязаны к семинару (оставлены, см. фильтр в админке)")


def fk_to_m2m(apps, schema_editor):
    Seminar = apps.get_model("seminars", "Seminar")
    SeminarReport = apps.get_model("seminars", "SeminarReport")
    Through = Seminar.reports.through
    Through.objects.bulk_create(
        Through(seminar_id=r.seminar_id, seminarreport_id=r.pk) for r in SeminarReport.objects.exclude(seminar_id=None)
    )


class Migration(migrations.Migration):

    dependencies = [
        ("seminars", "0029_department_fk_to_academy"),
        ("academy", "0002_restructure"),
    ]

    operations = [
        migrations.AddField(
            model_name="seminarreport",
            name="seminar",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="seminars.seminar",
                verbose_name="Семинар",
            ),
        ),
        immediate_constraints(),
        migrations.RunPython(m2m_to_fk, fk_to_m2m),
    ]
