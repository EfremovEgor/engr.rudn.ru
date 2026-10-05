# Уровни обучения и языки хранились русскими строками (и частично кодами из CSV-импорта).
# Приводим к кодам: bachelor/specialist/master/postgraduate и ru/en.
from django.db import migrations

LEVELS = {
    "бакалавриат": "bachelor",
    "специалитет": "specialist",
    "магистратура": "master",
    "аспирантура": "postgraduate",
}
LEVELS_BACK = {
    "bachelor": "Бакалавриат",
    "specialist": "Специалитет",
    "master": "Магистратура",
    "postgraduate": "Аспирантура",
}
LANGUAGES = {
    "ru": ["ru"],
    "рус": ["ru"],
    "русский": ["ru"],
    "russian": ["ru"],
    "en": ["en"],
    "англ": ["en"],
    "английский": ["en"],
    "english": ["en"],
    "русский и английский": ["ru", "en"],
}
LANGUAGES_BACK = {"ru": "Русский", "en": "Английский"}


def normalize(apps, schema_editor):
    for model_name in ("Profile", "StudyDirection"):
        model = apps.get_model("education", model_name)
        for obj in model.objects.all():
            code = LEVELS.get((obj.study_level or "").strip().lower())
            if code is None:
                if obj.study_level not in LEVELS_BACK:
                    print(f"\n  ! {model_name} #{obj.pk}: неизвестный уровень обучения «{obj.study_level}» оставлен как есть")
                continue
            obj.study_level = code
            obj.save(update_fields=["study_level"])

    Profile = apps.get_model("education", "Profile")
    for profile in Profile.objects.all():
        codes = []
        for value in profile.language_fields or []:
            mapped = LANGUAGES.get(str(value).strip().lower())
            if mapped is None:
                print(f"\n  ! программа #{profile.pk}: неизвестный язык «{value}» пропущен")
                continue
            codes.extend(code for code in mapped if code not in codes)
        profile.language_fields = sorted(codes, key=["ru", "en"].index) or ["ru"]
        profile.save(update_fields=["language_fields"])


def denormalize(apps, schema_editor):
    for model_name in ("Profile", "StudyDirection"):
        model = apps.get_model("education", model_name)
        for obj in model.objects.all():
            obj.study_level = LEVELS_BACK.get(obj.study_level, obj.study_level)
            obj.save(update_fields=["study_level"])
    Profile = apps.get_model("education", "Profile")
    for profile in Profile.objects.all():
        profile.language_fields = [LANGUAGES_BACK.get(code, code) for code in profile.language_fields or []]
        profile.save(update_fields=["language_fields"])


class Migration(migrations.Migration):

    dependencies = [
        ("education", "0004_exams"),
    ]

    operations = [
        migrations.RunPython(normalize, denormalize),
    ]
