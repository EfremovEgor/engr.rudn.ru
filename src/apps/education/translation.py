from modeltranslation.translator import register

from apps.core.translation import BaseTranslationOptions

from .models import AdditionalProgram, ExamSubject, Program, ProgramOffer, StudyDirection


@register(StudyDirection)
class StudyDirectionTranslation(BaseTranslationOptions):
    fields = ("name",)


@register(Program)
class ProgramTranslation(BaseTranslationOptions):
    fields = ("name", "content")


@register(ProgramOffer)
class ProgramOfferTranslation(BaseTranslationOptions):
    fields = ("note",)


@register(ExamSubject)
class ExamSubjectTranslation(BaseTranslationOptions):
    fields = ("name",)


@register(AdditionalProgram)
class AdditionalProgramTranslation(BaseTranslationOptions):
    fields = ("title", "description", "volume", "study_mode", "language", "information")
