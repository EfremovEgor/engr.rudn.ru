# Generated by Django 4.2.6 on 2023-11-01 17:05

from django.db import migrations, models
import django_jsonform.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_profile_job_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='job_title',
            field=django_jsonform.models.fields.ArrayField(base_field=models.CharField(max_length=255, verbose_name='Должность/Звание'), blank=True, null=True, size=20, verbose_name='Должности/Звания'),
        ),
    ]
