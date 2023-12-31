# Generated by Django 4.2.6 on 2023-11-01 17:00

import ckeditor_uploader.fields
import django.contrib.postgres.fields
from django.db import migrations, models
import django_jsonform.models.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.TextField(verbose_name='ФИО')),
                ('image', models.ImageField(upload_to='profiles', verbose_name='Фотография')),
                ('office', models.TextField(verbose_name='Кабинет')),
                ('emails', django_jsonform.models.fields.ArrayField(base_field=models.EmailField(max_length=255, verbose_name='Электронный адрес'), blank=True, null=True, size=10, verbose_name='Электронные адреса')),
                ('phone_numbers', django.contrib.postgres.fields.ArrayField(base_field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Номер телефона'), blank=True, null=True, size=10, verbose_name='Номера телефонов')),
                ('working_hours', models.CharField(blank=True, max_length=255, null=True, verbose_name='Рабочее время')),
                ('staff_support', django_jsonform.models.fields.JSONField(blank=True, null=True, verbose_name='Помощник')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Информация')),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
    ]
