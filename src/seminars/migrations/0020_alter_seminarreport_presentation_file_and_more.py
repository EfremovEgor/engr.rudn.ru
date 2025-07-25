# Generated by Django 5.2.1 on 2025-06-27 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seminars', '0019_alter_seminarreport_presentation_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seminarreport',
            name='presentation_file',
            field=models.URLField(blank=True, null=True, verbose_name='Presentation URL'),
        ),
        migrations.AlterField(
            model_name='seminarreport',
            name='video_recording',
            field=models.URLField(blank=True, null=True, verbose_name='Video recording URL'),
        ),
    ]
