from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext_lazy as _

from .models import DissertationCommittee, ScientificCenter


def centers(request):
    return render(
        request,
        "science/scientific_centers.html",
        {
            "title": _("Научные центры"),
            "centers": ScientificCenter.objects.published().select_related("head").order_by("position"),
        },
    )


def center_detail(request, slug):
    center = get_object_or_404(
        ScientificCenter.objects.published().select_related("head", "department"), slug=slug
    )
    # Пока подробное описание не заполнено в админке, показываем свёрстанную вручную страницу.
    if not center.content and center.legacy_template:
        template = f"science/centers/{center.legacy_template}"
    else:
        template = "science/scientific_center_item.html"
    return render(request, template, {"title": center.name, "center": center})


def dissertation_committees(request):
    return render(
        request,
        "science/dissertation_committees.html",
        {
            "title": _("Диссертационные советы"),
            "committees": DissertationCommittee.objects.prefetch_related("scientific_specialties").order_by("cipher"),
        },
    )


def dissertation_committee_detail(request, pk):
    committee = get_object_or_404(DissertationCommittee.objects.prefetch_related("scientific_specialties"), pk=pk)
    return render(
        request,
        "science/dissertation_committee_item.html",
        {"title": f"{_('ПДС')} {committee.cipher}", "committee": committee},
    )
