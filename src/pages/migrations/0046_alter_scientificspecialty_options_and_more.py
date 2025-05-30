# Generated by Django 5.1.6 on 2025-04-28 17:50

import django_jsonform.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0045_scientificcenters_brief_description_en_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='scientificspecialty',
            options={'ordering': ['cipher', 'name'], 'verbose_name': 'Научное направление', 'verbose_name_plural': 'Научные направления'},
        ),
        migrations.AddField(
            model_name='dissertationcommittee',
            name='address_en',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Адрес (EN)'),
        ),
        migrations.AddField(
            model_name='dissertationcommittee',
            name='chairman_en',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Председатель (EN)'),
        ),
        migrations.AddField(
            model_name='dissertationcommittee',
            name='composition_en',
            field=django_jsonform.models.fields.ArrayField(base_field=models.CharField(max_length=255, verbose_name='Участник диссовета (EN)'), blank=True, null=True, size=20, verbose_name='Состав диссовета (EN)'),
        ),
        migrations.AddField(
            model_name='dissertationcommittee',
            name='deputy_en',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Заместитель председателя (EN)'),
        ),
        migrations.AddField(
            model_name='dissertationcommittee',
            name='faculty_en',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Факультет (EN)'),
        ),
        migrations.AddField(
            model_name='dissertationcommittee',
            name='organization_en',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Организация (EN)'),
        ),
        migrations.AddField(
            model_name='dissertationcommittee',
            name='secretary_en',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Секретарь (EN)'),
        ),
        migrations.AddField(
            model_name='scientificspecialty',
            name='name_en',
            field=models.TextField(blank=True, null=True, verbose_name='Название (EN)'),
        ),
        migrations.AlterField(
            model_name='dissertationcommittee',
            name='address',
            field=models.CharField(default='115419, Москва, улица Орджоникидзе, 3', max_length=255, verbose_name='Адрес (RU)'),
        ),
        migrations.AlterField(
            model_name='dissertationcommittee',
            name='chairman',
            field=models.CharField(max_length=255, verbose_name='Председатель (RU)'),
        ),
        migrations.AlterField(
            model_name='dissertationcommittee',
            name='composition',
            field=django_jsonform.models.fields.ArrayField(base_field=models.CharField(max_length=255, verbose_name='Участник диссовета (RU)'), blank=True, null=True, size=20, verbose_name='Состав диссовета'),
        ),
        migrations.AlterField(
            model_name='dissertationcommittee',
            name='deputy',
            field=models.CharField(max_length=255, verbose_name='Заместитель председателя (RU)'),
        ),
        migrations.AlterField(
            model_name='dissertationcommittee',
            name='faculty',
            field=models.CharField(default='Инженерная академия', max_length=255, verbose_name='Факультет (RU)'),
        ),
        migrations.AlterField(
            model_name='dissertationcommittee',
            name='organization',
            field=models.CharField(default='Российский университет дружбы народов', max_length=255, verbose_name='Организация (RU)'),
        ),
        migrations.AlterField(
            model_name='dissertationcommittee',
            name='secretary',
            field=models.CharField(max_length=255, verbose_name='Секретарь (RU)'),
        ),
        migrations.AlterField(
            model_name='scientificspecialty',
            name='name',
            field=models.TextField(verbose_name='Название (RU)'),
        ),
    ]
