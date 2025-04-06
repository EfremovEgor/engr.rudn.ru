from django.forms import model_to_dict
from django.shortcuts import render
from .models import (
    DepartmentInfo,
    IndexContact,
    Profile,
    AdministrationProfiles,
    StudyDirection,
    DissertationCommittee,
    ScientificCenters,
    MainSlider,
)
from django.http import Http404, HttpResponse
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
from profiles.models import StudentCommitteeProfile
from .utils import aliases, functions
from django.utils.translation import gettext as _
import re

def index(request):
    slider_images = MainSlider.objects.all()
    news = NewsItem.objects.prefetch_related().order_by("-creation_date")[:10]
    return render(
        request,
        "pages/index.html",
        {
            "title": _("Инженерная академия РУДН"),
            "contacts": list(IndexContact.objects.order_by("position").all()),
            "news": news,
            "slider_images": slider_images,
        },
    )


class NewsView(View):
    template_name = "pages/news.html"

    def get(self, request):
        news = NewsItem.objects.prefetch_related().order_by("-creation_date")[:30]        
        tags = Tag.objects.filter(newsitem__tags__isnull=False).distinct()
        return render(
            request,
            self.template_name,
            {
                "title": _("Новости"),
                "news": news,
                "tags": tags,
            },
        )

    def post(self, request, *args, **kwargs):
        search_details = {
            "searched_title": (
                request.POST.get("title") if request.POST.get("title") else ""
            ),
            "searched_tags": (
                request.POST.get("tags") if request.POST.get("tags") else ""
            ),
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
                "title": _("Новости"),
                "news": news,
                "tags": tags,
                **search_details,
            },
        )


class NewsItemView(View):
    template_name = "pages/news_item_page.html"

    def get(self, request, id):
        news_item = get_object_or_404(NewsItem, pk=id)
        if request.LANGUAGE_CODE == 'en':
            page_title = news_item.title_en or _("Untitled")
        else:
            page_title = news_item.title_ru or _("Без названия")

        return render(
            request,
            self.template_name,
            {
                "title": page_title,
                "content": news_item,
            },
        )


def news(request):
    news = NewsItem.objects.prefetch_related().order_by("creation_date")
    tags = Tag.objects.filter(newsitem__tags__isnull=False).distinct()
    return render(
        request,
        "pages/news.html",
        {
            "title": _("Новости"),
            "news": news,
            "tags": tags,
        },
    )


def directions(request, id):
    profile_object = get_object_or_404(Profile, pk=id)
    profile_data = model_to_dict(profile_object)
    direction = StudyDirection.objects.filter(profiles__in=[profile_object]).first()
    profile_data["direction"] = direction
    if profile_object.faculty_field is not None:
        profile_data["faculty"] = model_to_dict(profile_object.faculty_field)
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
        {"title": profile_object.name, "profile_data": profile_data},
    )


def academy(request):
    return render(
        request,
        "pages/academy/academy.html",
        {
            "title": _("Академия"),
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
            "title": _("Дирекция"),
            "profiles": data,
        },
    )


def history(request):
    return render(
        request,
        "pages/academy/history.html",
        {
            "title": _("История"),
        },
    )


def science_directions(request):
    return render(
        request,
        "pages/science/directions.html",
        {
            "title": _("Научные направления"),
        },
    )


def science_journals(request):
    return render(
        request,
        "pages/science/journals.html",
        {
            "title": _("Научные журналы"),
        },
    )


def scientific_student_society(request):
    return render(
        request,
        "pages/science/scientific_student_society.html",
        {
            "title": _("Научное студенческое общество"),
        },
    )


def science_events(request):
    return render(
        request,
        "pages/science/events.html",
        {
            "title": _("Научные мероприятия"),
        },
    )

def science_seminars(request):
    return render(
        request,
        "pages/science/seminars.html",
        {
            "title": _("Научные семинары"),
        },
    )

def science_cits(request):
    return render(
        request,
        "pages/science/cits.html",
        {
            "title": _("Конференция по информационным и техническим системам"),
        },
    )

def science_scitechforum(request):
    return render(
        request,
        "pages/science/scitechforum.html",
        {
            "title": _("Международный научно-технический форум по механике космического полета и космическим конструкциям и материалам"),
        },
    )


def graduates_contacts(request):
    return render(
        request,
        "pages/graduates/contacts.html",
        {
            "title": _("Контакты"),
        },
    )


def digital_library(request):
    return render(
        request,
        "pages/science/digital_library.html",
        {
            "title": _("Электронная библиотека"),
        },
    )


def graduates_topics_of_dissertation_research(request):
    return render(
        request,
        "pages/graduates/topics_of_dissertation_research.html",
        {
            "title": _("Тематики диссертационных исследований"),
        },
    )


def students_applications(request):
    applications = StudentsApplications.objects.order_by("position").all()
    return render(
        request,
        "pages/students/applications.html",
        {
            "title": _("Образцы заявлений"),
            "applications": applications,
        },
    )


def students_schedule(request):
    return render(
        request,
        "pages/students/schedule.html",
        {
            "title": _("Расписание"),
        },
    )


def students_student_committee(request):
    profiles = StudentCommitteeProfile.objects.order_by("position").all()

    return render(
        request,
        "pages/students/student_committee.html",
        {
            "title": _("Студенческий комитет"),
            "profiles": profiles,
        },
    )


def applicants_reference(request):
    cis = ApplicantsCISNormativeDocument.objects.all()
    foreign = ApplicantsForeignNormativeDocument.objects.all()
    return render(
        request,
        "pages/applicants/reference.html",
        {
            "title": _("Справочная информация"),
            "cis": cis,
            "foreign": foreign,
        },
    )


def open_days(request):
    presentations = OpenDaysFiles.objects.filter(type=_("Презентация")).all()
    return render(
        request,
        "pages/applicants/open_days.html",
        {
            "title": _("Дни открытых дверей"),
            "presentations": presentations,
        },
    )


def study_directions(request):
    return render(
        request,
        "pages/applicants/study_directions.html",
        {
            "title": _("Направления подготовки"),
        },
    )


def levels_of_study(request, level):
    levels = {
        "bachelor": _("Бакалавриат"),
        "masters": _("Магистратура"),
        "postgraduates": _("Аспирантура"),
        "specialists": _("Специалитет"),
    }
    if level not in levels:
        return HttpResponse(status=404)

    def natural_sort_key(s):
        return [
            int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', s.cipher)
        ]

    directions = list(
        StudyDirection.objects.filter(study_level=levels[level])
    )
    directions.sort(key=natural_sort_key)

    for direction in directions:
        profiles = list(direction.profiles.all())

        profiles.sort(key=lambda s: [
            int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', s.cipher or '')
        ])


        direction.sorted_profiles = profiles

    return render(
        request,
        f"pages/applicants/levels/{level}.html",
        {
            "title": levels[level],
            "directions": directions,
        },
    )


def committee(request):
    return render(
        request,
        "pages/applicants/committee.html",
        {
            "title": _("Приемная комиссия"),
        },
    )


def dissertation_committees(request):
    committees = DissertationCommittee.objects.order_by("cipher").all()
    return render(
        request,
        "pages/students/dissertation_committees.html",
        {
            "title": _("Диссертационные советы"),
            "committees": committees,
        },
    )


def scientific_centers(request):
    centers = ScientificCenters.objects.all().order_by("position")
    return render(
        request,
        "pages/science/scientific_centers.html",
        {
            "title": _("Научные центры"),
            "centers": centers,
        },
    )


def scientific_center_item(request, name):
    center = get_object_or_404(ScientificCenters, page_url=name)
    alias = aliases.scientific_center_name_to_page.get(
        " ".join(word.strip() for word in center.name.split())
    )

    if alias is None:
        raise Http404

    return render(
        request,
        f"pages/science/scientific_centers/{alias}",
        {
            "title": center.name,
            "center": center,
        },
    )


def dissertation_committee(request, id):
    committee = get_object_or_404(DissertationCommittee, pk=id)

    return render(
        request,
        "pages/students/dissertation_committee_item.html",
        {
            "title": f"{_('ПДС')} {committee.cipher}",
            "committee": committee,
        },
    )


def departments(request):
    departments = DepartmentInfo.objects.order_by("position").all()
    return render(
        request,
        "pages/academy/departments.html",
        {
            "title": _("Кафедры"),
            "departments": departments,
        },
    )


def department_item(request, name):
    abb = aliases.department_abbreviation_to_name.get(name)
    if abb is None:
        raise Http404

    department = get_object_or_404(DepartmentInfo, abbreviation=abb)
    bachelors = (
        StudyDirection.objects.filter(
            profiles__faculty_field=department, profiles__study_level=_("Бакалавриат")
        )
        .distinct()
        .all()
    )
    masters = (
        StudyDirection.objects.filter(
            profiles__faculty_field=department, profiles__study_level=_("Магистратура")
        )
        .distinct()
        .all()
    )
    specialty = (
        StudyDirection.objects.filter(
            profiles__faculty_field=department, profiles__study_level=_("Специалитет")
        )
        .distinct()
        .all()
    )
    postgraduates = (
        StudyDirection.objects.filter(
            profiles__faculty_field=department, profiles__study_level=_("Аспирантура")
        )
        .distinct()
        .all()
    )
    scientific_centers = ScientificCenters.objects.filter(faculty_field=department)

    staff = department.staff.order_by("position").all()
    return render(
        request,
        "pages/academy/department_item.html",
        {
            "title": department.name,
            "department": department,
            "bachelors": bachelors,
            "masters": masters,
            "specialty": specialty,
            "postgraduates": postgraduates,
            "scientific_centers": scientific_centers,
            "staff": staff,
        },
    )


def contacts(request):
    return render(
        request,
        "pages/academy/contacts.html",
        {
            "title": _("Контакты"),
        },
    )