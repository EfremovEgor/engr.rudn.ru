# Минимальные баллы: два JSON-поля превращены в строки «предмет — балл бюджет / балл контракт».
# Предметы вынесены в справочник ExamSubject — их название переводится один раз для всех программ.
import django.db.models.deletion
from django.db import migrations, models

from apps.core.migration_utils import immediate_constraints

KIND_BY_KEY = {
    "Обязательные предметы": "required",
    "Дополнительные предметы (один на выбор)": "optional",
}


def _records(data, key):
    if not isinstance(data, dict):
        return []
    records = data.get(key) or []
    return records if isinstance(records, list) else []


def scores_to_rows(apps, schema_editor):
    ProfileDetails = apps.get_model("education", "ProfileDetails")
    ExamSubject = apps.get_model("education", "ExamSubject")
    OfferExam = apps.get_model("education", "OfferExam")
    subjects = {}

    def subject_for(name):
        clean = " ".join(name.split())
        key = clean.casefold()
        if key not in subjects:
            subjects[key] = ExamSubject.objects.create(name=clean, name_ru=clean)
        return subjects[key]

    rows = []
    for details in ProfileDetails.objects.order_by("id"):
        budget = details.minimal_passing_scores_budget
        contract = details.minimal_passing_scores_contract
        keys = list(KIND_BY_KEY)
        for data in (budget, contract):
            if isinstance(data, dict):
                for key in data:
                    if key not in keys:
                        print(f"\n  ! условия #{details.pk}: неизвестный раздел баллов «{key}» — считаю обязательным")
                        keys.append(key)
        for key in keys:
            kind = KIND_BY_KEY.get(key, "required")
            order, by_budget, by_contract = [], {}, {}
            for source, target in ((budget, by_budget), (contract, by_contract)):
                for record in _records(source, key):
                    if not isinstance(record, dict):
                        continue
                    name = str(record.get("subject") or "").strip()
                    if not name:
                        continue
                    score = record.get("score")
                    target[name] = "" if score is None else str(score).strip()
                    if name not in order:
                        order.append(name)
            for position, name in enumerate(order):
                rows.append(
                    OfferExam(
                        offer_id=details.pk,
                        subject=subject_for(name),
                        kind=kind,
                        score_budget=by_budget.get(name, ""),
                        score_contract=by_contract.get(name, ""),
                        position=position,
                    )
                )
    OfferExam.objects.bulk_create(rows)


def rows_to_scores(apps, schema_editor):
    ProfileDetails = apps.get_model("education", "ProfileDetails")
    OfferExam = apps.get_model("education", "OfferExam")
    key_by_kind = {v: k for k, v in KIND_BY_KEY.items()}
    for details in ProfileDetails.objects.all():
        exams = OfferExam.objects.filter(offer_id=details.pk).select_related("subject").order_by("kind", "position")
        budget = {key: [] for key in KIND_BY_KEY}
        contract = {key: [] for key in KIND_BY_KEY}
        for exam in exams:
            key = key_by_kind[exam.kind]
            if exam.score_budget:
                budget[key].append({"subject": exam.subject.name, "score": exam.score_budget})
            if exam.score_contract:
                contract[key].append({"subject": exam.subject.name, "score": exam.score_contract})
        details.minimal_passing_scores_budget = budget if any(budget.values()) else None
        details.minimal_passing_scores_contract = contract if any(contract.values()) else None
        details.save()


class Migration(migrations.Migration):

    dependencies = [
        ("education", "0003_offers"),
    ]

    operations = [
        migrations.CreateModel(
            name="ExamSubject",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, verbose_name="Предмет")),
                ("name_ru", models.CharField(max_length=255, null=True, verbose_name="Предмет [ru]")),
                ("name_en", models.CharField(blank=True, max_length=255, null=True, verbose_name="Предмет [en]")),
            ],
            options={
                "verbose_name": "Вступительное испытание (предмет)",
                "verbose_name_plural": "Вступительные испытания (предметы)",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="OfferExam",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "kind",
                    models.CharField(
                        choices=[("required", "Обязательный"), ("optional", "По выбору")],
                        default="required",
                        max_length=16,
                        verbose_name="Тип",
                    ),
                ),
                ("score_budget", models.CharField(blank=True, default="", max_length=255, verbose_name="Мин. балл (бюджет)")),
                ("score_contract", models.CharField(blank=True, default="", max_length=255, verbose_name="Мин. балл (контракт)")),
                ("position", models.PositiveIntegerField(default=0, verbose_name="Позиция")),
                (
                    "offer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="exams",
                        to="education.profiledetails",
                        verbose_name="Условия приёма",
                    ),
                ),
                (
                    "subject",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="exams",
                        to="education.examsubject",
                        verbose_name="Предмет",
                    ),
                ),
            ],
            options={
                "verbose_name": "Минимальный балл",
                "verbose_name_plural": "Минимальные баллы",
                "ordering": ["-kind", "position", "id"],
            },
        ),
        immediate_constraints(),
        migrations.RunPython(scores_to_rows, rows_to_scores),
        migrations.RemoveField(model_name="profiledetails", name="minimal_passing_scores_budget"),
        migrations.RemoveField(model_name="profiledetails", name="minimal_passing_scores_contract"),
        migrations.RemoveField(model_name="profiledetails", name="name"),
        migrations.RemoveField(model_name="profiledetails", name="name_en"),
    ]
