from django.forms import model_to_dict
from django.shortcuts import render
from .models import IndexContact, Profile, AdministrationProfiles, StudyDirection
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from news.models import NewsItem, Tag
from django.views import View
from django.shortcuts import get_object_or_404
from documents.models import (
    ApplicantsCISNormativeDocument,
    ApplicantsForeignNormativeDocument,
    OpenDaysFiles,
    StudentsApplications,
)


def index(request):
    news = NewsItem.objects.prefetch_related().order_by("creation_date")[:10]
    return render(
        request,
        "pages/index.html",
        {
            "title": "Инженерная академия РУДН",
            "contacts": list(IndexContact.objects.order_by("position").all()),
            "news": news,
        },
    )


class NewsView(View):
    template_name = "pages/news.html"

    def get(self, request):
        news = NewsItem.objects.prefetch_related().order_by("creation_date")[:30]

        tags = Tag.objects.filter(newsitem__tags__isnull=False).distinct()
        return render(
            request,
            self.template_name,
            {
                "title": "Новости",
                "news": news,
                "tags": tags,
            },
        )

    def post(self, request, *args, **kwargs):
        search_details = {
            "searched_title": request.POST.get("title")
            if request.POST.get("title")
            else "",
            "searched_tags": request.POST.get("tags")
            if request.POST.get("tags")
            else "",
        }

        to_search = {}
        if title := request.POST.get("title"):
            to_search["title__icontains"] = title

        if tag := request.POST.get("tags"):
            if tag:
                tag = Tag.objects.filter(name=tag).first()
                if tag is not None:
                    to_search["tags__in"] = [tag]
                else:
                    to_search["tags__in"] = []
        news = (
            NewsItem.objects.prefetch_related()
            .filter(**to_search)
            .order_by("creation_date")
        )

        tags = Tag.objects.filter(newsitem__tags__isnull=False).distinct()

        return render(
            request,
            "pages/news.html",
            {
                "title": "Новости",
                "news": news,
                "tags": tags,
                **search_details,
            },
        )


class NewsItemView(View):
    template_name = "pages/news_item_page.html"

    def get(self, request, id):
        content = get_object_or_404(NewsItem, pk=id)
        return render(
            request,
            self.template_name,
            {
                "title": content.title,
                "content": content,
            },
        )


def news(request):
    news = NewsItem.objects.prefetch_related().order_by("creation_date")
    tags = Tag.objects.filter(newsitem__tags__isnull=False).distinct()
    return render(
        request,
        "pages/news.html",
        {
            "title": "Новости",
            "news": news,
            "tags": tags,
        },
    )


def directions(request, id):
    profile_object = get_object_or_404(Profile, pk=id)
    profile_data = model_to_dict(profile_object)
    direction = StudyDirection.objects.filter(profiles__in=[profile_object]).first()
    profile_data["direction"] = direction
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


def scientific_student_society(request):
    return render(
        request,
        "pages/science/scientific_student_society.html",
        {
            "title": "Научные студенческое общество",
        },
    )


def science_seminars(request):
    return render(
        request,
        "pages/science/seminars.html",
        {
            "title": "Научные семинары",
        },
    )


def graduates_contacts(request):
    return render(
        request,
        "pages/graduates/contacts.html",
        {
            "title": "Контакты",
        },
    )


def graduates_digital_library(request):
    return render(
        request,
        "pages/graduates/digital_library.html",
        {
            "title": "Электронная библиотека",
        },
    )


def graduates_topics_of_dissertation_research(request):
    return render(
        request,
        "pages/graduates/topics_of_dissertation_research.html",
        {
            "title": "Тематики диссертационных исследований",
        },
    )


def students_applications(request):
    applications = StudentsApplications.objects.order_by("position").all()
    return render(
        request,
        "pages/students/applications.html",
        {
            "title": "Образцы заявлений",
            "applications": applications,
        },
    )


def students_schedule(request):
    return render(
        request,
        "pages/students/schedule.html",
        {
            "title": "Расписание",
        },
    )


def students_student_committee(request):
    return render(
        request,
        "pages/students/student_committee.html",
        {
            "title": "Студенческий коммитет",
        },
    )


def applicants_reference(request):
    cis = ApplicantsCISNormativeDocument.objects.all()
    foreign = ApplicantsForeignNormativeDocument.objects.all()
    return render(
        request,
        "pages/applicants/reference.html",
        {
            "title": "Справочная информация",
            "cis": cis,
            "foreign": foreign,
        },
    )


def open_days(request):
    presentations = OpenDaysFiles.objects.filter(type="Презентация").all()
    print(presentations)
    return render(
        request,
        "pages/applicants/open_days.html",
        {
            "title": "Дни открытых дверей",
            "presentations": presentations,
        },
    )


def study_directions(request):
    return render(
        request,
        "pages/applicants/study_directions.html",
        {
            "title": "Направления подготовки",
        },
    )


def levels_of_study(request, level):
    levels = {
        "bachelor": "Бакалавриат",
        "masters": "Магистратура",
        "postgraduates": "Аспирантура",
        "specialists": "Специалитет",
    }
    if level not in levels:
        return HttpResponse(status=404)
    directions = StudyDirection.objects.filter(study_level=levels[level])
    return render(
        request,
        f"pages/applicants/levels/{level}.html",
        {
            "title": levels[level],
            "directions": directions,
        },
    )
