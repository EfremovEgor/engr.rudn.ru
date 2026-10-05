from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.academy.models import Department
from apps.education.models import AdditionalProgram, Program
from apps.news.models import NewsItem
from apps.pages.models import Page
from apps.pages.views import STATIC_PAGES
from apps.science.models import ScientificCenter
from apps.seminars.models import Seminar


class StaticSitemap(Sitemap):
    i18n = True
    changefreq = "monthly"

    def items(self):
        return ["pages:index", *[f"pages:{name}" for name in STATIC_PAGES], "news:news_list", "academy:departments",
                "academy:administration", "education:study_directions", "science:centers", "seminars:seminars_list"]

    def location(self, item):
        return reverse(item)


class ModelSitemap(Sitemap):
    i18n = True
    changefreq = "weekly"

    def __init__(self, queryset):
        self.queryset = queryset
        super().__init__()

    def items(self):
        return [obj for obj in self.queryset.all() if obj.get_absolute_url()]


sitemaps = {
    "static": StaticSitemap,
    "news": ModelSitemap(NewsItem.objects.published()),
    "programs": ModelSitemap(Program.objects.published()),
    "additional": ModelSitemap(AdditionalProgram.objects.published()),
    "departments": ModelSitemap(Department.objects.exclude(slug=None)),
    "centers": ModelSitemap(ScientificCenter.objects.published().exclude(slug=None)),
    "seminars": ModelSitemap(Seminar.objects.published()),
    "pages": ModelSitemap(Page.objects.published()),
}
