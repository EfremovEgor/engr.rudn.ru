from modeltranslation.translator import register

from apps.core.translation import BaseTranslationOptions

from .models import Seminar, SeminarReport, SeminarSpeaker


@register(SeminarSpeaker)
class SeminarSpeakerTranslation(BaseTranslationOptions):
    fields = ("last_name", "first_name", "middle_name", "job_title", "academic_title", "academic_degree", "bio")


@register(Seminar)
class SeminarTranslation(BaseTranslationOptions):
    fields = ("name", "description")


@register(SeminarReport)
class SeminarReportTranslation(BaseTranslationOptions):
    fields = ("name", "annotation")
