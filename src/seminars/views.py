from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from .models import Seminar


def seminars(request):
    seminars = Seminar.objects.all()
    return render(
        request,
        "seminars.html",
        {"title": "Семинары", "seminars": seminars},
    )
