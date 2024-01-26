from django.contrib import admin
from .models import (
    ApplicantsCISNormativeDocument,
    ApplicantsForeignNormativeDocument,
    OpenDaysFiles,
    StudentsApplications,
)

admin.site.register(ApplicantsCISNormativeDocument)
admin.site.register(ApplicantsForeignNormativeDocument)
admin.site.register(OpenDaysFiles)
admin.site.register(StudentsApplications)
