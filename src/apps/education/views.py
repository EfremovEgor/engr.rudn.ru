import re

from django.db.models import Prefetch
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext_lazy as _

from .models import AdditionalProgram, Program, StudyDirection, StudyLanguage, StudyLevel, TranslatorModule

#: Адреса разделов (сохранены прежние) -> уровни обучения в БД
LEVEL_PAGES = {
    "bachelor": {
        "levels": [StudyLevel.BACHELOR, StudyLevel.SPECIALIST],
        "title": _("Бакалавриат/Специалитет"),
        "desc": _("Открытие новых горизонтов знаний!"),
    },
    "specialists": {
        "levels": [StudyLevel.SPECIALIST],
        "title": _("Специалитет"),
        "desc": _("Превратите свои увлечения в профессию!"),
    },
    "masters": {
        "levels": [StudyLevel.MASTER],
        "title": _("Магистратура"),
        "desc": _("Углублённое изучение вашей специализации!"),
    },
    "postgraduates": {
        "levels": [StudyLevel.POSTGRADUATE],
        "title": _("Аспирантура"),
        "desc": _("Станьте экспертом в своей области!"),
    },
}


def _program_language(request) -> str:
    lang = request.GET.get("prog_lang", StudyLanguage.RU)
    return lang if lang in StudyLanguage.values else StudyLanguage.RU


def natural_key(value: str):
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r"(\d+)", value or "")]


def study_directions(request):
    program_lang = _program_language(request)
    sections = []
    for slug, page in LEVEL_PAGES.items():
        has_programs = Program.objects.published().filter(
            study_level__in=page["levels"], languages__contains=[program_lang]
        ).exists()
        sections.append({"slug": slug, "title": page["title"], "desc": page["desc"], "has_en": has_programs})
    if program_lang == StudyLanguage.EN:
        sections = [s for s in sections if s["has_en"]]
    sections.sort(key=lambda s: not s["has_en"])
    return render(
        request,
        "education/study_directions.html",
        {"sections": sections, "current_lang": program_lang, "title": _("Программы подготовки")},
    )


def levels_of_study(request, level):
    page = LEVEL_PAGES.get(level)
    if page is None:
        raise Http404
    program_lang = _program_language(request)
    programs = Program.objects.published().filter(languages__overlap=[program_lang])
    directions = (
        StudyDirection.objects.filter(study_level__in=page["levels"], programs__in=programs)
        .distinct()
        .prefetch_related(Prefetch("programs", queryset=programs, to_attr="filtered_programs"))
    )
    order = {lvl: index for index, lvl in enumerate(page["levels"])}
    directions = sorted(directions, key=lambda d: (order.get(d.study_level, 99), natural_key(d.cipher)))
    for direction in directions:
        direction.sorted_profiles = sorted(direction.filtered_programs, key=lambda p: natural_key(p.cipher or p.name))
    return render(
        request,
        f"education/levels/{level}.html",
        {"title": page["title"], "directions": directions, "current_lang": program_lang},
    )


def program_detail(request, pk):
    program = get_object_or_404(
        Program.objects.published()
        .select_related("direction", "department")
        .prefetch_related("offers__exams__subject"),
        pk=pk,
    )
    offers = program.offers_list
    return render(
        request,
        "education/program_detail.html",
        {
            "title": program.name,
            "program": program,
            "offers": offers,
            "duration": next((o.study_duration for o in offers if o.study_duration), None),
            "level_slug": "bachelor"
            if program.study_level in (StudyLevel.BACHELOR, StudyLevel.SPECIALIST)
            else {StudyLevel.MASTER: "masters", StudyLevel.POSTGRADUATE: "postgraduates"}.get(program.study_level),
            "exams_only": program.study_level in (StudyLevel.MASTER, StudyLevel.POSTGRADUATE),
        },
    )


def translator_module(request):
    module = TranslatorModule.objects.select_related(
        "contact_employee1__related_profile", "contact_employee2__related_profile"
    ).first()
    if module is None:
        raise Http404
    return render(
        request,
        "education/translator_module.html",
        {"title": _("Модуль переводчика"), "program": module},
    )


def additional_programs(request):
    return render(
        request,
        "education/additional_programs.html",
        {
            "title": _("Программы дополнительного профессионального образования"),
            "programs": AdditionalProgram.objects.published().select_related("department"),
        },
    )


def additional_program_detail(request, pk):
    item = get_object_or_404(
        AdditionalProgram.objects.published().select_related(
            "department", "program_director__related_profile", "contact_person__related_profile"
        ),
        pk=pk,
    )
    return render(request, "education/additional_program_detail.html", {"title": item.title, "item": item})
