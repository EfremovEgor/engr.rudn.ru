from django.forms import model_to_dict
from django.shortcuts import render
from ..models import (
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
from ..utils import aliases, functions


def index(request):
    from django import urls

    url_resolver = urls.get_resolver(urls.get_urlconf())

    print(url_resolver.namespace_dict.keys())
    slider_images = MainSlider.objects.all()
    news = NewsItem.objects.prefetch_related().order_by("-creation_date")[:10]
    return render(
        request,
        "en/pages/index.html",
        {
            "title": "Engineering Academy Of RUDN",
            "contacts": list(IndexContact.objects.order_by("position").all()),
            "news": news,
            "slider_images": slider_images,
        },
    )


class NewsView(View):
    template_name = "en/pages/news.html"

    def get(self, request):
        news = NewsItem.objects.prefetch_related().order_by("-creation_date")[:30]

        tags = Tag.objects.filter(newsitem__tags__isnull=False).distinct()
        return render(
            request,
            self.template_name,
            {
                "title": "News",
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
            to_search["title_en__icontains"] = title

        if tag := request.POST.get("tags"):
            if tag:
                tag = Tag.objects.filter(name_en=tag).first()
                if tag is not None:
                    to_search["tags__in"] = [tag]
                else:
                    to_search["tags__in"] = []
        news = (
            NewsItem.objects.prefetch_related()
            .filter(**to_search)
            .order_by("-creation_date")
        )

        tags = Tag.objects.filter(newsitem__tags__isnull=False).distinct()

        return render(
            request,
            "en/pages/news.html",
            {
                "title": "News",
                "news": news,
                "tags": tags,
                **search_details,
            },
        )


class NewsItemView(View):
    template_name = "en/pages/news_item_page.html"

    def get(self, request, id):
        content = get_object_or_404(NewsItem, pk=id)
        return render(
            request,
            self.template_name,
            {
                "title": content.title_en,
                "content": content,
            },
        )


def news(request):
    news = NewsItem.objects.prefetch_related().order_by("creation_date")
    tags = Tag.objects.filter(newsitem__tags__isnull=False).distinct()
    return render(
        request,
        "en/pages/news.html",
        {
            "title": "News",
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
        "en/pages/academy/academy.html",
        {
            "title": "Academy",
        },
    )


def administration(request):
    profile_objects = AdministrationProfiles.objects.order_by("position").all()
    data = list()
    for profile in profile_objects:
        data.append(model_to_dict(profile.employee))
    return render(
        request,
        "en/pages/academy/administration.html",
        {
            "title": "Administration",
            "profiles": data,
        },
    )


def history(request):
    return render(
        request,
        "en/pages/academy/history.html",
        {
            "title": "History",
        },
    )


def science_directions(request):
    return render(
        request,
        "en/pages/science/directions.html",
        {
            "title": "Scientific Directions",
        },
    )


def science_journals(request):
    return render(
        request,
        "en/pages/science/journals.html",
        {
            "title": "Scientific Journals",
        },
    )


def scientific_student_society(request):
    return render(
        request,
        "en/pages/science/scientific_student_society.html",
        {
            "title": "Scientific Student Society",
        },
    )


def science_events(request):
    return render(
        request,
        "en/pages/science/events.html",
        {
            "title": "Scientific Events",
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


def science_cits(request):
    return render(
        request,
        "en/pages/science/cits.html",
        {
            "title": "SCO/CIS Conference on Information and Technical Systems",
        },
    )


def science_scitechforum(request):
    return render(
        request,
        "en/pages/science/scitechforum.html",
        {
            "title": "BRICS SCITECH FORUM",
        },
    )


def graduates_contacts(request):
    return render(
        request,
        "en/pages/graduates/contacts.html",
        {
            "title": "Contacts",
        },
    )


def digital_library(request):
    return render(
        request,
        "en/pages/science/digital_library.html",
        {
            "title": "Digital Library",
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
        "en/pages/students/applications.html",
        {
            "title": "Sample Applications",
            "applications": applications,
        },
    )


def students_schedule(request):
    return render(
        request,
        "en/pages/students/schedule.html",
        {
            "title": "Class Schedule",
        },
    )


def students_student_committee(request):
    profiles = StudentCommitteeProfile.objects.order_by("position").all()

    return render(
        request,
        "en/pages/students/student_committee.html",
        {
            "title": "Student Committee",
            "profiles": profiles,
        },
    )


def applicants_reference(request):
    cis = ApplicantsCISNormativeDocument.objects.all()
    foreign = ApplicantsForeignNormativeDocument.objects.all()
    return render(
        request,
        "en/pages/applicants/reference.html",
        {
            "title": "Admission of Foreign Citizens",
            "cis": cis,
            "foreign": foreign,
        },
    )


def open_days(request):
    presentations = OpenDaysFiles.objects.filter(type="Презентация").all()
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
        "en/pages/applicants/study_directions.html",
        {
            "title": "Educational Programs",
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

    directions = (
        StudyDirection.objects.filter(study_level=levels[level])
        .order_by("cipher")
        .all()
    )
    directions_ = []
    for direction in directions:
        direction_ = direction.__dict__
        direction_["profiles"] = direction.profiles.all().order_by(
            "cipher", "-language_fields", "-name"
        )
        directions_.append(direction_)
    return render(
        request,
        f"pages/applicants/levels/{level}.html",
        {
            "title": levels[level],
            "directions": directions_,
        },
    )


def committee(request):
    return render(
        request,
        "en/pages/applicants/committee.html",
        {
            "title": "Admissions Committee",
        },
    )


def dissertation_committees(request):
    committees = DissertationCommittee.objects.order_by("cipher").all()
    return render(
        request,
        "en/pages/students/dissertation_committees.html",
        {
            "title": "Dissertation Committee",
            "committees": committees,
        },
    )


def scientific_centers(request):
    centers = ScientificCenters.objects.all().order_by("position")
    return render(
        request,
        "en/pages/science/scientific_centers.html",
        {
            "title": "Scientific Centers",
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
            "title": f"ПДС {committee.cipher}",
            "committee": committee,
        },
    )


def departments(request):
    departments = DepartmentInfo.objects.order_by("position").all()
    return render(
        request,
        "en/pages/academy/departments.html",
        {
            "title": "Department",
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
            profiles__faculty_field=department, profiles__study_level="Бакалавриат"
        )
        .distinct()
        .all()
    )
    masters = (
        StudyDirection.objects.filter(
            profiles__faculty_field=department, profiles__study_level="Магистратура"
        )
        .distinct()
        .all()
    )
    specialty = (
        StudyDirection.objects.filter(
            profiles__faculty_field=department, profiles__study_level="Специалитет"
        )
        .distinct()
        .all()
    )
    postgraduates = (
        StudyDirection.objects.filter(
            profiles__faculty_field=department, profiles__study_level="Аспирантура"
        )
        .distinct()
        .all()
    )
    scientific_centers = ScientificCenters.objects.filter(faculty_field=department)

    staff = department.staff.order_by("position").all()
    return render(
        request,
        "en/pages/academy/department_item.html",
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
        "en/pages/academy/contacts.html",
        {
            "title": "Contacts",
        },
    )
