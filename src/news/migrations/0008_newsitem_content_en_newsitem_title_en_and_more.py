# Generated by Django 5.1.6 on 2025-05-13 14:51

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0007_alter_newsitem_creation_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="newsitem",
            name="content_en",
            field=ckeditor_uploader.fields.RichTextUploadingField(
                blank=True, null=True, verbose_name="Content"
            ),
        ),
        migrations.AddField(
            model_name="newsitem",
            name="title_en",
            field=models.TextField(
                blank=True, null=True, unique=True, verbose_name="Name"
            ),
        ),
        migrations.AlterField(
            model_name="newsitem",
            name="content",
            field=ckeditor_uploader.fields.RichTextUploadingField(
                blank=True, null=True, verbose_name="Информация"
            ),
        ),
        migrations.AlterField(
            model_name="newsitem",
            name="title",
            field=models.TextField(
                blank=True, null=True, unique=True, verbose_name="Название"
            ),
        ),
    ]
