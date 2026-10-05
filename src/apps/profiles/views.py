from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext_lazy as _

from .models import EmployeeProfile, StudentCommitteeProfile


def profile(request, pk):
    employee = get_object_or_404(EmployeeProfile, pk=pk)
    return render(request, "profiles/profile.html", {"title": employee.full_name, "employee": employee})


def student_committee(request):
    return render(
        request,
        "profiles/student_committee.html",
        {"title": _("Студенческий комитет"), "profiles": StudentCommitteeProfile.objects.order_by("position")},
    )
