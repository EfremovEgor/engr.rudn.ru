from django import forms
from django.contrib import admin
from django.shortcuts import redirect
from unfold.decorators import display
from unfold.widgets import UnfoldAdminCheckboxSelectMultipleWidget

from apps.core.admin.base import BaseAdmin, BaseStackedInline, BaseTabularInline, PublishableAdmin

from .models import (
    AdditionalProgram,
    ExamSubject,
    OfferExam,
    Program,
    ProgramOffer,
    StudyDirection,
    StudyLanguage,
    TranslatorModule,
)


class ProgramInline(BaseTabularInline):
    model = Program
    fields = ("name", "cipher", "department", "is_published")
    autocomplete_fields = ("department",)


@admin.register(StudyDirection)
class StudyDirectionAdmin(BaseAdmin):
    list_display = ("cipher", "name", "study_level", "programs_count")
    list_display_links = ("cipher", "name")
    list_filter = ("study_level",)
    search_fields = ("cipher", "name_ru", "name_en")
    fieldsets = ((None, {"fields": (("cipher", "study_level"),)}),)
    inlines = [ProgramInline]

    @display(description="Программ")
    def programs_count(self, obj):
        return obj.programs.count()


class ProgramForm(forms.ModelForm):
    languages = forms.MultipleChoiceField(
        label="Языки обучения",
        choices=StudyLanguage.choices,
        widget=UnfoldAdminCheckboxSelectMultipleWidget,
    )

    class Meta:
        model = Program
        fields = "__all__"


class ProgramOfferInline(BaseStackedInline):
    model = ProgramOffer
    fields = (
        ("study_form", "study_duration"),
        ("budget_places", "paid_places"),
        ("price_first_year", "price_second_year", "price_third_year"),
        ("price_fourth_year", "price_fifth_year", "price_sixth_year"),
        "admission_url",
    )
    extra = 0
    show_change_link = True
    verbose_name_plural = "Условия приёма по формам обучения (баллы и примечание — по ссылке «Изменить»)"


@admin.register(Program)
class ProgramAdmin(PublishableAdmin):
    form = ProgramForm
    list_display = ("name", "direction", "study_level", "department", "forms", "published")
    list_filter = ("study_level", "is_published", "department", "direction")
    search_fields = ("name_ru", "name_en", "cipher", "direction__cipher", "direction__name_ru")
    autocomplete_fields = ("direction", "department")
    list_select_related = ("direction", "department")
    fieldsets = (
        (None, {"fields": ("direction", ("cipher", "study_level"), "department", "languages", "is_published")}),
    )
    inlines = [ProgramOfferInline]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("offers")

    @display(description="Формы обучения")
    def forms(self, obj):
        return ", ".join(offer.get_study_form_display() for offer in obj.offers_list) or "—"


class OfferExamInline(BaseTabularInline):
    model = OfferExam
    fields = ("kind", "subject", "score_budget", "score_contract", "position")
    autocomplete_fields = ("subject",)
    ordering_field = "position"
    hide_ordering_field = True
    show_change_link = False


@admin.register(ProgramOffer)
class ProgramOfferAdmin(BaseAdmin):
    list_display = ("__str__", "study_form", "budget_places", "study_duration")
    list_filter = ("study_form", ("program", admin.EmptyFieldListFilter), "program__study_level")
    search_fields = ("program__name_ru", "program__name_en")
    autocomplete_fields = ("program",)
    list_select_related = ("program",)
    fieldsets = (
        (None, {"fields": ("program", ("study_form", "study_duration"), ("budget_places", "paid_places"), "admission_url")}),
        (
            "Стоимость обучения по контракту",
            {
                "fields": (
                    ("price_first_year", "price_second_year", "price_third_year"),
                    ("price_fourth_year", "price_fifth_year", "price_sixth_year"),
                )
            },
        ),
    )
    inlines = [OfferExamInline]


@admin.register(ExamSubject)
class ExamSubjectAdmin(BaseAdmin):
    list_display = ("__str__", "name_ru", "name_en", "usage")
    list_editable = ("name_ru", "name_en")
    search_fields = ("name_ru", "name_en")

    @display(description="Используется")
    def usage(self, obj):
        return obj.exams.count()


@admin.register(AdditionalProgram)
class AdditionalProgramAdmin(PublishableAdmin):
    list_display = ("title", "department", "cost", "published")
    list_filter = ("is_published", "department")
    search_fields = ("title_ru", "title_en")
    autocomplete_fields = ("department", "program_director", "contact_person")
    ordering_field = "position"
    hide_ordering_field = True
    ordering = ("position",)
    fieldsets = (
        (None, {"fields": ("department", ("program_director", "contact_person"), "cost", "is_published", "position")}),
    )


@admin.register(TranslatorModule)
class TranslatorModuleAdmin(BaseAdmin):
    autocomplete_fields = ("contact_employee1", "contact_employee2")

    def has_add_permission(self, request):
        return not TranslatorModule.objects.exists() and super().has_add_permission(request)

    def changelist_view(self, request, extra_context=None):
        obj = TranslatorModule.objects.first()
        if obj is not None:
            return redirect("admin:education_translatormodule_change", obj.pk)
        return super().changelist_view(request, extra_context)
