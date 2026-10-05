from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext_lazy as _

from apps.education.models import Program, StudyDirection, StudyLevel

from .models import AdministrationMember, Department


def administration(request):
    members = AdministrationMember.objects.select_related("employee").order_by("position")
    return render(
        request,
        "academy/administration.html",
        {"title": _("Дирекция"), "profiles": [member.employee for member in members]},
    )


def departments(request):
    return render(
        request,
        "academy/departments.html",
        {
            "title": _("Кафедры"),
            "departments": Department.objects.select_related("head__related_profile").order_by("position"),
        },
    )


def department_detail(request, slug):
    department = get_object_or_404(
        Department.objects.select_related("head__related_profile", "contact_employee__related_profile"),
        slug=slug,
    )
    programs = Program.objects.published().filter(department=department)
    directions = (
        StudyDirection.objects.filter(programs__in=programs)
        .distinct()
        .prefetch_related(Prefetch("programs", queryset=programs, to_attr="department_programs"))
        .order_by("cipher")
    )
    by_level = {level: [] for level in StudyLevel.values}
    for direction in directions:
        by_level.setdefault(direction.study_level, []).append(direction)
    return render(
        request,
        "academy/department_item.html",
        {
            "title": department.name,
            "department": department,
            "bachelors": by_level[StudyLevel.BACHELOR],
            "specialty": by_level[StudyLevel.SPECIALIST],
            "masters": by_level[StudyLevel.MASTER],
            "postgraduates": by_level[StudyLevel.POSTGRADUATE],
            "scientific_centers": department.scientific_centers.published().select_related("head"),
            "staff": department.staff.select_related("related_profile").order_by("position"),
        },
    )
