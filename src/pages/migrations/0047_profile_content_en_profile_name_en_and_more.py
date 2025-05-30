# Generated by Django 5.1.6 on 2025-04-29 09:33

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0046_alter_scientificspecialty_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='content_en',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Информация (EN)'),
        ),
        migrations.AddField(
            model_name='profile',
            name='name_en',
            field=models.TextField(blank=True, null=True, verbose_name='Название (EN)'),
        ),
        migrations.AddField(
            model_name='profiledetails',
            name='name_en',
            field=models.TextField(blank=True, null=True, verbose_name='Название (EN)'),
        ),
        migrations.AddField(
            model_name='studydirection',
            name='name_en',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Название (EN)'),
        ),
    ]
