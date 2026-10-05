"""Миграции реструктуризации на данных в старой схеме (как на продакшене до обновления)."""

from decimal import Decimal

from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TransactionTestCase

OLD_STATE = [
    ("pages", "0058_additionaleducationitem_description"),
    ("profiles", "0023_alter_employeeprofile_phone_numbers"),
    ("seminars", "0028_seminarreport_video"),
    ("news", "0011_newsitem_tags_en_alter_newsitem_tags"),
    ("documents", "0007_applicantscisnormativedocument_name_en_and_more"),
    ("academy", None),
    ("education", None),
    ("science", None),
    ("media_library", None),
]


class RestructureMigrationTests(TransactionTestCase):
    def setUp(self):
        executor = MigrationExecutor(connection)
        self.new_state = executor.loader.graph.leaf_nodes()
        executor.migrate(OLD_STATE)
        self.old_apps = executor.loader.project_state(OLD_STATE[:5]).apps

    def tearDown(self):
        executor = MigrationExecutor(connection)
        executor.loader.build_graph()
        executor.migrate(executor.loader.graph.leaf_nodes())

    def migrate_forward(self):
        executor = MigrationExecutor(connection)
        executor.loader.build_graph()
        executor.migrate(self.new_state)
        return executor.loader.project_state(self.new_state).apps

    def test_old_data_is_converted(self):
        old = self.old_apps
        Department = old.get_model("pages", "DepartmentInfo")
        Profile = old.get_model("pages", "Profile")
        Details = old.get_model("pages", "ProfileDetails")
        Direction = old.get_model("pages", "StudyDirection")
        Seminar = old.get_model("seminars", "Seminar")
        Report = old.get_model("seminars", "SeminarReport")
        Tag = old.get_model("news", "Tag")
        News = old.get_model("news", "NewsItem")
        Cis = old.get_model("documents", "ApplicantsCISNormativeDocument")

        dept = Department.objects.create(name="Кафедра", name_en="Dept", position=1, abbreviation="КМПУ", info="i")
        scores = {"Обязательные предметы": [{"subject": "Математика", "score": "40"}],
                  "Дополнительные предметы (один на выбор)": [{"subject": "Физика", "score": "41"}]}
        contract = {"Обязательные предметы": [{"subject": "Математика", "score": "39"}],
                    "Дополнительные предметы (один на выбор)": [{"subject": "Физика", "score": "41"}]}
        shared = Details.objects.create(name="d", study_duration=Decimal("4"), budget_places=10,
                                        minimal_passing_scores_budget=scores, minimal_passing_scores_contract=contract)
        p1 = Profile.objects.create(name="Мехатроника", name_en="Mechatronics", study_level="Бакалавриат",
                                    language_fields=["Русский и английский"], faculty_field=dept,
                                    full_time_details=shared, content="c")
        p2 = Profile.objects.create(name="Робототехника", study_level="Магистратура", language_fields=["en"],
                                    extramural_details=shared, content="c")
        direction = Direction.objects.create(name="Направление", study_level="Бакалавриат", cipher="15.03.06")
        direction.profiles.set([p1, p2])

        s1 = Seminar.objects.create(name="Семинар 1", position=None)
        s2 = Seminar.objects.create(name="Семинар 2", position=2)
        report = Report.objects.create(name="Доклад", week=1, speaker=None)
        s1.reports.add(report)
        s2.reports.add(report)

        ru, en = Tag.objects.create(name="Наука"), Tag.objects.create(name="Science")
        news = News.objects.create(title="Новость", title_en="News", content="t")
        news.tags.add(ru)
        news.tags_en.add(en)
        Cis.objects.create(name="Правила", name_en="Rules", file="documents/r.pdf")

        new = self.migrate_forward()

        Department = new.get_model("academy", "Department")
        dept = Department.objects.get()
        self.assertEqual((dept.slug, dept.name_ru, dept.name_en), ("kmpu", "Кафедра", "Dept"))

        Program = new.get_model("education", "Program")
        p1 = Program.objects.get(name_ru="Мехатроника")
        p2 = Program.objects.get(name_ru="Робототехника")
        self.assertEqual((p1.study_level, p1.languages, p1.department_id), ("bachelor", ["ru", "en"], dept.pk))
        self.assertEqual((p2.study_level, p2.languages), ("master", ["en"]))
        self.assertEqual(p1.direction_id, p2.direction_id)

        Offer = new.get_model("education", "ProgramOffer")
        o1 = Offer.objects.get(program=p1)
        o2 = Offer.objects.get(program=p2)
        self.assertNotEqual(o1.pk, o2.pk)  # общая запись условий приёма скопирована
        self.assertEqual((o1.study_form, o2.study_form), ("full_time", "extramural"))
        Exam = new.get_model("education", "OfferExam")
        rows = sorted(Exam.objects.filter(offer=o1).values_list("subject__name_ru", "kind", "score_budget", "score_contract"))
        self.assertEqual(rows, [("Математика", "required", "40", "39"), ("Физика", "optional", "41", "41")])

        Seminar = new.get_model("seminars", "Seminar")
        Report = new.get_model("seminars", "SeminarReport")
        self.assertEqual(Report.objects.count(), 2)
        self.assertEqual(Report.objects.filter(seminar__name_ru="Семинар 2").count(), 1)
        self.assertEqual(Seminar.objects.get(name_ru="Семинар 1").position, 0)

        Tag = new.get_model("news", "Tag")
        self.assertEqual(Tag.objects.get(name_en="Science").name_ru, None)
        News = new.get_model("news", "NewsItem")
        self.assertEqual(News.objects.get().tags.count(), 2)

        Document = new.get_model("documents", "Document")
        doc = Document.objects.get()
        self.assertEqual((doc.category, doc.name_ru, doc.name_en, doc.file_ru), ("applicants_cis", "Правила", "Rules", "documents/r.pdf"))
