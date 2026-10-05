from django.contrib import admin
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse

from apps.core.i18n import instance_translation_status, translation_status_q
from apps.news.models import NewsItem

from .factories import create_site_content

PUBLIC_URLS = [
    "/",
    "/academy",
    "/academy/history",
    "/academy/contacts",
    "/academy/administration",
    "/academy/departments",
    "/academy/departments/kmpu",
    "/applicants/committee",
    "/applicants/reference",
    "/applicants/open_days",
    "/applicants/study_directions",
    "/applicants/study_directions?prog_lang=en",
    "/applicants/study_directions?prog_lang=unknown",
    "/applicants/study_directions/bachelor",
    "/applicants/study_directions/masters",
    "/applicants/study_directions/postgraduates",
    "/applicants/study_directions/specialists",
    "/applicants/additional_education",
    "/applicants/additional_education/translator_module",
    "/applicants/additional_education/additional_professional_education",
    "/science/directions",
    "/science/journals",
    "/science/events",
    "/science/cits",
    "/science/scitechforum",
    "/science/digital_library",
    "/science/scientific_student_society",
    "/science/scientific_centers",
    "/science/scientific_centers/center",
    "/science/scientific_centers/photon",
    "/science/dissertation_committees",
    "/science/seminars/",
    "/graduates/contacts",
    "/graduates/topics_of_dissertation_research",
    "/students/schedule",
    "/students/appplications",
    "/students/student_committee",
    "/news/",
    "/news/?tag=Наука",
    "/about/new",
]


@override_settings(SERVE_MEDIA=False)
class PublicPagesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.objects = create_site_content()

    def detail_urls(self):
        o = self.objects
        return [
            f"/applicants/study_directions/{o['program'].pk}",
            f"/news/{o['news'].pk}",
            f"/profile/{o['employee'].pk}",
            f"/profile/{o['employee'].pk}/",
            f"/science/dissertation_committees/{o['committee'].pk}",
            f"/science/seminars/{o['seminar'].pk}/",
            f"/science/seminars/{o['seminar'].pk}/get_reports/",
            f"/science/seminars/{o['seminar'].pk}/reports/{o['seminar'].reports.get().uuid}/",
        ]

    def test_pages_open_in_both_languages(self):
        for prefix in ("", "/en"):
            for url in PUBLIC_URLS + self.detail_urls():
                with self.subTest(url=prefix + url):
                    response = self.client.get(prefix + url)
                    self.assertIn(response.status_code, (200, 301, 302), prefix + url)

    def test_program_page_shows_offer_and_exams(self):
        program = self.objects["program"]
        content = self.client.get(f"/applicants/study_directions/{program.pk}").content.decode()
        self.assertIn("Математика – 40 (39 – на контракт)", content)
        self.assertIn("Бюджетные места – 25", content)
        content_en = self.client.get(f"/en/applicants/study_directions/{program.pk}").content.decode()
        self.assertIn("Mechatronics", content_en)
        self.assertIn("Mathematics", content_en)

    def test_english_falls_back_to_russian(self):
        content = self.client.get("/en/academy/departments/kmpu").content.decode()
        self.assertIn("Department of Mechanics", content)
        # программа кафедры видна и на английской версии (раньше фильтр ломался)
        self.assertIn("Mechatronics", content)

    def test_unpublished_hidden(self):
        news = self.objects["news"]
        news.is_published = False
        news.save()
        self.assertEqual(self.client.get(f"/news/{news.pk}").status_code, 404)

    def test_unknown_page_is_404(self):
        self.assertEqual(self.client.get("/no/such/page").status_code, 404)


class AdminTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_site_content()
        cls.user = User.objects.create_superuser("root", "root@example.com", "pass")

    def setUp(self):
        self.client.force_login(self.user)

    def test_all_admin_pages_open(self):
        urls = [reverse("admin:index"), reverse("admin:translations_overview"), reverse("admin:media_library_mediafile_upload")]
        for model, model_admin in admin.site._registry.items():
            info = (model._meta.app_label, model._meta.model_name)
            urls.append(reverse("admin:%s_%s_changelist" % info))
            urls.append(reverse("admin:%s_%s_changelist" % info) + "?translation_en=missing")
            if model_admin.has_add_permission(type("R", (), {"user": self.user})()):
                urls.append(reverse("admin:%s_%s_add" % info))
            obj = model._default_manager.first()
            if obj is not None:
                urls.append(reverse("admin:%s_%s_change" % info, args=[obj.pk]))
        for url in urls:
            with self.subTest(url=url):
                self.assertIn(self.client.get(url).status_code, (200, 302), url)

    def test_english_tab_shows_russian_hint(self):
        news = NewsItem.objects.first()
        content = self.client.get(reverse("admin:news_newsitem_change", args=[news.pk])).content.decode()
        self.assertIn("RU: Новость", content)


class TranslationStatusTests(TestCase):
    def test_status(self):
        full = NewsItem.objects.create(title_ru="а", title_en="a", content_ru="б", content_en="b")
        partial = NewsItem.objects.create(title_ru="а", title_en="a", content_ru="б")
        missing = NewsItem.objects.create(title_ru="а", content_ru="б")
        self.assertEqual(instance_translation_status(full, "en"), "complete")
        self.assertEqual(instance_translation_status(partial, "en"), "partial")
        self.assertEqual(instance_translation_status(missing, "en"), "missing")
        q = translation_status_q(NewsItem, "en")
        self.assertEqual(list(NewsItem.objects.filter(q["missing"])), [missing])
        self.assertEqual(list(NewsItem.objects.filter(q["partial"])), [partial])
        self.assertIn(full, NewsItem.objects.filter(q["complete"]))
