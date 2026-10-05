from decimal import Decimal

from apps.academy.models import AdministrationMember, Department
from apps.documents.models import Document
from apps.education.models import (
    AdditionalProgram,
    ExamSubject,
    OfferExam,
    Program,
    ProgramOffer,
    StudyDirection,
    TranslatorModule,
)
from apps.news.models import NewsItem, Tag
from apps.pages.models import IndexContact, MainSlider, Page
from apps.profiles.models import DepartmentStaff, EmployeeProfile, StudentCommitteeProfile
from apps.science.models import DissertationCommittee, ScientificCenter, ScientificSpecialty
from apps.seminars.models import Seminar, SeminarReport, SeminarSpeaker


def create_site_content():
    """Минимальный набор данных, при котором открываются все страницы сайта."""
    employee = EmployeeProfile.objects.create(
        full_name_ru="Иванов Иван", full_name_en="Ivan Ivanov", job_title_ru=["Директор"], emails=["i@rudn.ru"],
        phone_numbers=["+74959550952|1234"],
    )
    staff = DepartmentStaff.objects.create(related_profile=employee, department_responsibilities_ru=["Заведующий"])
    department = Department.objects.create(
        name_ru="Кафедра механики", name_en="Department of Mechanics", slug="kmpu", abbreviation="КМПУ",
        info_ru="Инфо", head=staff, contact_employee=staff,
    )
    department.staff.add(staff)
    AdministrationMember.objects.create(employee=employee, position=1)
    StudentCommitteeProfile.objects.create(full_name_ru="Студент", position=1, office="1", email="s@rudn.ru")

    direction = StudyDirection.objects.create(name_ru="Мехатроника и робототехника", study_level="bachelor", cipher="15.03.06")
    program = Program.objects.create(
        name_ru="Мехатроника", name_en="Mechatronics", study_level="bachelor", direction=direction,
        department=department, languages=["ru", "en"], content_ru="<p>Описание</p>",
    )
    offer = ProgramOffer.objects.create(
        program=program, study_form="full_time", budget_places=25, study_duration=Decimal("4"),
        price_first_year=400000, price_second_year=410000,
    )
    math = ExamSubject.objects.create(name_ru="Математика", name_en="Mathematics")
    OfferExam.objects.create(offer=offer, subject=math, score_budget="40", score_contract="39")
    TranslatorModule.objects.create(contact_employee1=staff)
    AdditionalProgram.objects.create(
        title_ru="Программа ДПО", volume_ru="72 часа", study_mode_ru="Очная", language_ru="Русский", cost=Decimal("1000"),
        department=department,
    )

    ScientificCenter.objects.create(name_ru="Центр", slug="center", head=employee, department=department, content_ru="<p>c</p>")
    ScientificCenter.objects.create(name_ru="Фотоника", slug="photon", legacy_template="photon.html", head=employee)
    specialty = ScientificSpecialty.objects.create(cipher="2.1.1", name_ru="Конструкции")
    committee = DissertationCommittee.objects.create(cipher="ПДС 1", chairman_ru="А", deputy_ru="Б", secretary_ru="В")
    committee.scientific_specialties.add(specialty)

    speaker = SeminarSpeaker.objects.create(last_name_ru="Петров", first_name_ru="Пётр")
    seminar = Seminar.objects.create(name_ru="Семинар", chair=employee, department=department)
    SeminarReport.objects.create(seminar=seminar, name_ru="Доклад", speaker=speaker, week=1)
    Seminar.objects.create(name_ru="Пустой семинар")

    tag = Tag.objects.create(name_ru="Наука", name_en="Science")
    news = NewsItem.objects.create(title_ru="Новость", title_en="News", content_ru="<p>Текст</p>")
    news.tags.add(tag)

    for category in Document.Category.values:
        Document.objects.create(category=category, name_ru=f"Документ {category}", file_ru="documents/a.pdf")
    MainSlider.objects.create(name_ru="Слайд", image_full_ru="main_slider_full/a.jpg", image_mobile_ru="m.jpg")
    IndexContact.objects.create(heading_ru="Приёмная", sub_heading_ru="Контакты")
    Page.objects.create(path="about/new", title_ru="Новая страница", content_ru="<p>Страница</p>")
    return {
        "employee": employee,
        "department": department,
        "program": program,
        "news": news,
        "seminar": seminar,
        "committee": committee,
    }
