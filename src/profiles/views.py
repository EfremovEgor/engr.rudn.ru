from django.forms import model_to_dict
from django.shortcuts import get_object_or_404, render
from .models import EmployeeProfile


def profiles(request, id):
    profile_object = get_object_or_404(EmployeeProfile, pk=id)
    profile_data = model_to_dict(profile_object)
    return render(
        request,
        "profile.html",
        {"title": profile_object.full_name, "employee": profile_data},
    )
