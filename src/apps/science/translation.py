from modeltranslation.translator import register

from apps.core.translation import BaseTranslationOptions

from .models import DissertationCommittee, Equipment, Partner, ScientificCenter, ScientificSpecialty


@register(ScientificCenter)
class ScientificCenterTranslation(BaseTranslationOptions):
    fields = ("name", "field_name", "brief_description", "content")


@register(Equipment)
class EquipmentTranslation(BaseTranslationOptions):
    fields = ("name", "purpose")


@register(Partner)
class PartnerTranslation(BaseTranslationOptions):
    fields = ("name", "collaboration_direction", "result", "about")


@register(ScientificSpecialty)
class ScientificSpecialtyTranslation(BaseTranslationOptions):
    fields = ("name",)


@register(DissertationCommittee)
class DissertationCommitteeTranslation(BaseTranslationOptions):
    fields = ("organization", "faculty", "address", "chairman", "deputy", "secretary", "composition")
