# Направление ↔ профиль: связь many-to-many заменена на внешний ключ Program.direction
# (профиль всегда принадлежит одному направлению; в админке профили редактируются внутри направления).
import django.db.models.deletion
from django.db import migrations, models

from apps.core.migration_utils import immediate_constraints


def m2m_to_fk(apps, schema_editor):
    StudyDirection = apps.get_model("education", "StudyDirection")
    Profile = apps.get_model("education", "Profile")
    Through = StudyDirection.profiles.through
    assigned = {}
    for row in Through.objects.order_by("studydirection_id", "id"):
        if row.profile_id in assigned:
            if assigned[row.profile_id] != row.studydirection_id:
                print(
                    f"\n  ! профиль #{row.profile_id} был в нескольких направлениях; "
                    f"оставлено направление #{assigned[row.profile_id]}, связь с #{row.studydirection_id} снята"
                )
            continue
        assigned[row.profile_id] = row.studydirection_id
        Profile.objects.filter(pk=row.profile_id).update(direction_id=row.studydirection_id)


def fk_to_m2m(apps, schema_editor):
    StudyDirection = apps.get_model("education", "StudyDirection")
    Profile = apps.get_model("education", "Profile")
    Through = StudyDirection.profiles.through
    Through.objects.bulk_create(
        Through(studydirection_id=p.direction_id, profile_id=p.pk)
        for p in Profile.objects.exclude(direction_id=None)
    )


class Migration(migrations.Migration):

    dependencies = [
        ("education", "0001_move_from_pages"),
        ("academy", "0002_restructure"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="direction",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="programs",
                to="education.studydirection",
                verbose_name="Направление подготовки",
            ),
        ),
        immediate_constraints(),
        migrations.RunPython(m2m_to_fk, fk_to_m2m),
        migrations.RemoveField(model_name="studydirection", name="profiles"),
    ]
