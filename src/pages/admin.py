from django.contrib import admin
from django_json_widget.widgets import JSONEditorWidget
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget

from .models import *


@admin.register(ProfileDetails)
class ProfileDetailsAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }


admin.site.register(IndexContact)
admin.site.register(Profile)
admin.site.register(StudyDirection)
