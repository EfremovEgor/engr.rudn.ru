from django.contrib import admin
from .models import Seminar, SeminarReport, SeminarSpeaker

admin.site.register(Seminar)
admin.site.register(SeminarReport)
admin.site.register(SeminarSpeaker)
