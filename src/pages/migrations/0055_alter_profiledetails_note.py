# Generated by Django 5.2.1 on 2025-07-19 16:43

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0054_alter_departmentinfo_job_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profiledetails',
            name='note',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', verbose_name='Примечание'),
        ),
    ]
