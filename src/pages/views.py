import os
from django.forms import model_to_dict
from django.shortcuts import render
from .models import IndexContact, Profile, AdministrationProfiles
from django.http import Http404
from django.shortcuts import get_object_or_404


def index(request):
    return render(
        request,
        "pages/index.html",
        {
            "title": "Инженерная академия РУДН",
            "contacts": list(IndexContact.objects.order_by("position").all()),
        },
    )


def news(request):
    return render(
        request,
        "pages/news.html",
        {
            "title": "Новости",
        },
    )


def directions(request, id):
    profile_object = get_object_or_404(Profile, pk=id)
    profile_data = model_to_dict(profile_object)
    profile_data["full_time_details"] = (
        model_to_dict(profile_object.full_time_details)
        if profile_data["full_time_details"] is not None
        else None
    )
    profile_data["part_time_details"] = (
        model_to_dict(profile_object.part_time_details)
        if profile_data["part_time_details"] is not None
        else None
    )
    profile_data["extramural_details"] = (
        model_to_dict(profile_object.extramural_details)
        if profile_data["extramural_details"] is not None
        else None
    )
    return render(
        request,
        "pages/direction.html",
        {"title": "Направление подготовки", "profile_data": profile_data},
    )


def academy(request):
    return render(
        request,
        "pages/academy/academy.html",
        {
            "title": "Академия",
        },
    )


def administration(request):
    profile_objects = AdministrationProfiles.objects.order_by("position").all()
    data = list()
    for profile in profile_objects:
        data.append(model_to_dict(profile.employee))
    return render(
        request,
        "pages/academy/administration.html",
        {
            "title": "Дирекция",
            "profiles": data,
        },
    )


def history(request):
    return render(
        request,
        "pages/academy/history.html",
        {
            "title": "История",
        },
    )


def science_directions(request):
    return render(
        request,
        "pages/science/directions.html",
        {
            "title": "Направления",
        },
    )


def science_journals(request):
    return render(
        request,
        "pages/science/journals.html",
        {
            "title": "Научные журналы",
        },
    )


def scientific_student_clubs(request):
    return render(
        request,
        "pages/science/scientific_student_clubs.html",
        {
            "title": "Научные студенческие кружки",
        },
    )


def science_seminars(request):
    return render(
        request,
        "pages/science/seminars.html",
        {
            "title": "Семинары",
        },
    )
