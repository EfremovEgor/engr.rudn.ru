# Generated by Django 5.0.1 on 2024-02-12 00:27

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_alter_newsitem_preview_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsitem',
            name='creation_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Название'),
        ),
    ]