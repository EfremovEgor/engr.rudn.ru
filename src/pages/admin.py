from tkinter import E
from django.contrib import admin
from django.db.models.functions import Lower


from .models import *


admin.site.register(ProfileDetails)
admin.site.register(IndexContact)
admin.site.register(Profile)
admin.site.register(StudyDirection)
admin.site.register(AdministrationProfiles)
admin.site.register(DissertationCommittee)
admin.site.register(ScientificSpecialty)
admin.site.register(DepartmentInfo)
admin.site.register(ScientificCenters)
admin.site.register(EquipmentData)
admin.site.register(PartnerData)
