# Условия приёма (бывш. ProfileDetails) теперь принадлежат программе и знают свою форму обучения,
# вместо трёх внешних ключей Profile.full_time_details / part_time_details / extramural_details.
import django.db.models.deletion
from django.db import migrations, models

from apps.core.migration_utils import immediate_constraints

FORMS = [
    ("full_time", "full_time_details_id"),
    ("part_time", "part_time_details_id"),
    ("extramural", "extramural_details_id"),
]


def link_offers(apps, schema_editor):
    Profile = apps.get_model("education", "Profile")
    ProfileDetails = apps.get_model("education", "ProfileDetails")
    for profile in Profile.objects.order_by("id"):
        for form, attr in FORMS:
            details_id = getattr(profile, attr)
            if details_id is None:
                continue
            details = ProfileDetails.objects.get(pk=details_id)
            if details.program_id is not None:
                # Одни и те же условия были привязаны к нескольким программам/формам — делаем копию.
                details.pk = None
                details.id = None
                details._state.adding = True
            details.program_id = profile.pk
            details.study_form = form
            details.save()
    orphans = ProfileDetails.objects.filter(program_id=None).count()
    if orphans:
        print(f"\n  ! {orphans} записей условий приёма не привязаны ни к одной программе (оставлены, см. фильтр в админке)")


def unlink_offers(apps, schema_editor):
    Profile = apps.get_model("education", "Profile")
    ProfileDetails = apps.get_model("education", "ProfileDetails")
    for details in ProfileDetails.objects.exclude(program_id=None):
        attr = dict(FORMS)[details.study_form]
        Profile.objects.filter(pk=details.program_id).update(**{attr: details.pk})


class Migration(migrations.Migration):

    dependencies = [
        ("education", "0002_program_direction_fk"),
    ]

    operations = [
        migrations.AddField(
            model_name="profiledetails",
            name="program",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="offers",
                to="education.profile",
                verbose_name="Программа",
            ),
        ),
        migrations.AddField(
            model_name="profiledetails",
            name="study_form",
            field=models.CharField(
                choices=[("full_time", "Очная"), ("part_time", "Очно-заочная"), ("extramural", "Заочная")],
                default="full_time",
                max_length=16,
                verbose_name="Форма обучения",
            ),
        ),
        immediate_constraints(),
        migrations.RunPython(link_offers, unlink_offers),
        migrations.RemoveField(model_name="profile", name="full_time_details"),
        migrations.RemoveField(model_name="profile", name="part_time_details"),
        migrations.RemoveField(model_name="profile", name="extramural_details"),
    ]
