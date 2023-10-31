import os
from django.forms import model_to_dict
from django.shortcuts import render
from .models import IndexContact, Profile
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


def profile(request, id):
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
        "pages/profile.html",
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
    return render(
        request,
        "pages/academy/administration.html",
        {
            "title": "Дирекция",
        },
    )


# def pages(request, folder, page):
#     page_obj = get_object_or_404(Pages, url=f"{folder}/{page}")
#     return render(
#         request,
#         f"pages/{folder}/{page}.html",
#         {
#             "title": page_obj.name,
#         },
#     )


# def folders(request, folder):
#     page_obj = get_object_or_404(Pages, url=f"{folder}")
#     if not os.path.exists(
#         os.path.join(
#             os.getcwd(), "pages", "templates", "pages", folder, f"{folder}.html"
#         )
#     ):
#         raise Http404
#     return render(
#         request,
#         f"pages/{folder}/{folder}.html",
#         {
#             "title": "Новости",
#         },
#     )
