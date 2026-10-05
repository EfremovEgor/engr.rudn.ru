# Перенос моделей из приложения pages в science.
# Только состояние Django: таблицы БД остаются прежними (db_table), данные не трогаются.
# ContentType и права переносятся, чтобы сохранить права групп и историю админки.

import django.db.models.deletion
import django_jsonform.models.fields
import phonenumber_field.modelfields
from django.db import migrations, models

from apps.core.migration_utils import move_content_type


class Migration(migrations.Migration):

    dependencies = [
        ("academy", "0001_move_from_pages"),
        ("pages", "0058_additionaleducationitem_description"),
        ("profiles", "0023_alter_employeeprofile_phone_numbers"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name='ScientificSpecialty',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('cipher', models.CharField(max_length=255, verbose_name='Шифр')),
                        ('name', models.TextField(verbose_name='Название (RU)')),
                        ('name_en', models.TextField(blank=True, null=True, verbose_name='Название (EN)')),
                    ],
                    options={
                        'ordering': ['cipher', 'name'],
                        'verbose_name': 'Научное направление',
                        'verbose_name_plural': 'Научные направления',
                        'db_table': 'pages_scientificspecialty',
                    },
                ),
                migrations.CreateModel(
                    name='DissertationCommittee',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('cipher', models.CharField(max_length=255, verbose_name='Шифр совета')),
                        ('faculty', models.CharField(default='Инженерная академия', max_length=255, verbose_name='Факультет (RU)')),
                        ('address', models.CharField(default='115419, Москва, улица Орджоникидзе, 3', max_length=255, verbose_name='Адрес (RU)')),
                        ('chairman', models.CharField(max_length=255, verbose_name='Председатель (RU)')),
                        ('secretary', models.CharField(max_length=255, verbose_name='Секретарь (RU)')),
                        ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Телефон')),
                        ('email', models.EmailField(blank=True, max_length=255, null=True, verbose_name='Электронная почта')),
                        ('composition', django_jsonform.models.fields.ArrayField(base_field=models.CharField(max_length=255, verbose_name='Участник диссовета (RU)'), blank=True, null=True, size=20, verbose_name='Состав диссовета')),
                        ('scientific_specialties', models.ManyToManyField(blank=True, to='science.scientificspecialty', verbose_name='Научные специальности')),
                        ('deputy', models.CharField(max_length=255, verbose_name='Заместитель председателя (RU)')),
                        ('organization', models.CharField(default='Российский университет дружбы народов', max_length=255, verbose_name='Организация (RU)')),
                        ('address_en', models.CharField(blank=True, max_length=255, null=True, verbose_name='Адрес (EN)')),
                        ('chairman_en', models.CharField(blank=True, max_length=255, null=True, verbose_name='Председатель (EN)')),
                        ('composition_en', django_jsonform.models.fields.ArrayField(base_field=models.CharField(max_length=255, verbose_name='Участник диссовета (EN)'), blank=True, null=True, size=20, verbose_name='Состав диссовета (EN)')),
                        ('deputy_en', models.CharField(blank=True, max_length=255, null=True, verbose_name='Заместитель председателя (EN)')),
                        ('faculty_en', models.CharField(blank=True, max_length=255, null=True, verbose_name='Факультет (EN)')),
                        ('organization_en', models.CharField(blank=True, max_length=255, null=True, verbose_name='Организация (EN)')),
                        ('secretary_en', models.CharField(blank=True, max_length=255, null=True, verbose_name='Секретарь (EN)')),
                    ],
                    options={
                        'ordering': ['cipher'],
                        'verbose_name': 'Диссертационный совет',
                        'verbose_name_plural': 'Диссертационные советы',
                        'db_table': 'pages_dissertationcommittee',
                    },
                ),
                migrations.CreateModel(
                    name='EquipmentData',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('name', models.TextField(verbose_name='Название')),
                        ('prefix', models.CharField(blank=True, help_text='Для удобства поиска в админке', max_length=255, null=True, verbose_name='Префикс')),
                        ('image', models.ImageField(blank=True, null=True, upload_to='equipment', verbose_name='Фотография')),
                        ('purpose', models.TextField(verbose_name='Назначение')),
                    ],
                    options={
                        'verbose_name': 'Оборудование',
                        'verbose_name_plural': 'Оборудование',
                        'ordering': ['prefix', 'name'],
                        'db_table': 'pages_equipmentdata',
                    },
                ),
                migrations.CreateModel(
                    name='PartnerData',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('name', models.TextField(verbose_name='Наименование организации')),
                        ('prefix', models.CharField(blank=True, help_text='Для удобства поиска в админке', max_length=255, null=True, verbose_name='Префикс')),
                        ('image', models.ImageField(blank=True, null=True, upload_to='equipment', verbose_name='Фотография')),
                        ('collaboration_direction', models.TextField(verbose_name='Предмет сотрудничества')),
                        ('result', models.TextField(verbose_name='Результат сотрудничества')),
                        ('about', models.TextField(verbose_name='О партнёре')),
                        ('link', models.URLField(blank=True, max_length=255, null=True, verbose_name='Ссылка на сайт')),
                    ],
                    options={
                        'verbose_name': 'Партнер',
                        'verbose_name_plural': 'Партнеры',
                        'ordering': ['prefix', 'name'],
                        'db_table': 'pages_partnerdata',
                    },
                ),
                migrations.CreateModel(
                    name='ScientificCenters',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('name', models.TextField(verbose_name='Название')),
                        ('brief_description', models.TextField(blank=True, null=True, verbose_name='Краткое описание')),
                        ('faculty_field', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='faculty_info_for_scientific_centers', to='academy.departmentinfo', verbose_name='Департамент/Кафедра')),
                        ('head', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.employeeprofile', verbose_name='Руководитель')),
                        ('position', models.IntegerField(verbose_name='Позиция')),
                        ('display', models.BooleanField(default=True, verbose_name='Видимость')),
                        ('email_fields', django_jsonform.models.fields.ArrayField(base_field=models.EmailField(max_length=255, verbose_name='Электронный адрес'), blank=True, null=True, size=10, verbose_name='Электронные адреса')),
                        ('field_name', models.TextField(blank=True, null=True, verbose_name='Сфера деятельности')),
                        ('page_url', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='Путь')),
                        ('brief_description_en', models.TextField(blank=True, null=True, verbose_name='Краткое описание (англ.)')),
                        ('field_name_en', models.TextField(blank=True, null=True, verbose_name='Сфера деятельности (англ.)')),
                        ('name_en', models.TextField(blank=True, null=True, verbose_name='Название (англ.)')),
                    ],
                    options={
                        'ordering': ['position', 'name'],
                        'verbose_name': 'Научный центр',
                        'verbose_name_plural': 'Научные центры',
                        'db_table': 'pages_scientificcenters',
                    },
                ),
            ],
            database_operations=[],
        ),
        move_content_type("pages", "scientificspecialty", "science", "scientificspecialty"),
        move_content_type("pages", "dissertationcommittee", "science", "dissertationcommittee"),
        move_content_type("pages", "equipmentdata", "science", "equipmentdata"),
        move_content_type("pages", "partnerdata", "science", "partnerdata"),
        move_content_type("pages", "scientificcenters", "science", "scientificcenters"),
    ]
