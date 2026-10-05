# Перенос моделей из приложения pages в education.
# Только состояние Django: таблицы БД остаются прежними (db_table), данные не трогаются.
# ContentType и права переносятся, чтобы сохранить права групп и историю админки.

import apps.pages.migrations._compat
import django.db.models.deletion
import django_jsonform.models.fields
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
                    name='ProfileDetails',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('name', models.TextField(verbose_name='Название')),
                        ('budget_places', models.PositiveIntegerField(blank=True, null=True, verbose_name='Количество бюджетных мест')),
                        ('price_first_year', models.PositiveIntegerField(blank=True, null=True, verbose_name='Стоимость обучения по контракту(1 год)')),
                        ('price_second_year', models.PositiveIntegerField(blank=True, null=True, verbose_name='Стоимость обучения по контракту(2 год)')),
                        ('price_third_year', models.PositiveIntegerField(blank=True, null=True, verbose_name='Стоимость обучения по контракту(3 год)')),
                        ('price_fourth_year', models.PositiveIntegerField(blank=True, null=True, verbose_name='Стоимость обучения по контракту(4 год)')),
                        ('price_fifth_year', models.PositiveIntegerField(blank=True, null=True, verbose_name='Стоимость обучения по контракту(5 год)')),
                        ('price_sixth_year', models.PositiveIntegerField(blank=True, null=True, verbose_name='Стоимость обучения по контракту(6 год)')),
                        ('paid_places', models.PositiveIntegerField(blank=True, null=True, verbose_name='Количество платных мест')),
                        ('admission_url', models.URLField(blank=True, max_length=255, null=True, verbose_name='Ссылка на admission.rudn')),
                        ('minimal_passing_scores_budget', django_jsonform.models.fields.JSONField(blank=True, null=True, verbose_name='Минимальные проходные баллы на бюджет:')),
                        ('minimal_passing_scores_contract', django_jsonform.models.fields.JSONField(blank=True, null=True, verbose_name='Минимальные проходные баллы на контракт:')),
                        ('study_duration', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True, verbose_name='Продолжительность обучения')),
                        ('name_en', models.TextField(blank=True, null=True, verbose_name='Название (EN)')),
                        ('note', models.TextField(blank=True, default='', verbose_name='Примечание')),
                    ],
                    options={
                        'verbose_name': 'Информация по профилю направления подготовки',
                        'verbose_name_plural': 'Информация по профилям направления подготовки',
                        'db_table': 'pages_profiledetails',
                    },
                ),
                migrations.CreateModel(
                    name='Profile',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('name', models.TextField(verbose_name='Название')),
                        ('cipher', models.CharField(blank=True, max_length=255, null=True, verbose_name='Шифр')),
                        ('study_level', models.CharField(choices=[('Бакалавриат', 'Бакалавриат'), ('Специалитет', 'Специалитет'), ('Магистратура', 'Магистратура'), ('Аспирантура', 'Аспирантура')], max_length=255, verbose_name='Уровень обучения')),
                        ('extramural_details', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='extramural_details', to='education.profiledetails', verbose_name='Информация по заочной форме обучения')),
                        ('full_time_details', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='full_time_details', to='education.profiledetails', verbose_name='Информация по очной форме обучения')),
                        ('part_time_details', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='part_time_details', to='education.profiledetails', verbose_name='Информация по очно-заочной форме обучения')),
                        ('content', models.TextField(verbose_name='Информация')),
                        ('language_fields', django_jsonform.models.fields.ArrayField(base_field=models.CharField(choices=[('Русский', 'Русский'), ('Английский', 'Английский'), ('Русский и английский', 'Русский и английский')], max_length=255, verbose_name='Язык обучения'), default=apps.pages.migrations._compat.get_languages, size=None)),
                        ('faculty_field', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='department_info', to='academy.departmentinfo', verbose_name='Департамент/Кафедра')),
                        ('content_en', models.TextField(blank=True, null=True, verbose_name='Информация (EN)')),
                        ('name_en', models.TextField(blank=True, null=True, verbose_name='Название (EN)')),
                    ],
                    options={
                        'verbose_name': 'Профиль направления',
                        'verbose_name_plural': 'Профили направления',
                        'db_table': 'pages_profile',
                    },
                ),
                migrations.CreateModel(
                    name='StudyDirection',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('name', models.CharField(max_length=255, verbose_name='Название')),
                        ('study_level', models.CharField(choices=[('Бакалавриат', 'Бакалавриат'), ('Специалитет', 'Специалитет'), ('Магистратура', 'Магистратура'), ('Аспирантура', 'Аспирантура')], max_length=255, verbose_name='Уровень обучения')),
                        ('cipher', models.CharField(max_length=255, verbose_name='Шифр')),
                        ('profiles', models.ManyToManyField(blank=True, to='education.profile', verbose_name='Профили')),
                        ('name_en', models.CharField(blank=True, max_length=255, null=True, verbose_name='Название (EN)')),
                    ],
                    options={
                        'verbose_name': 'Направление подготовки',
                        'verbose_name_plural': 'Направления подготовки',
                        'db_table': 'pages_studydirection',
                    },
                ),
                migrations.CreateModel(
                    name='AdditionalEducation',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('contact_employee1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contact_employee1', to='profiles.departmentstaff', verbose_name='Контактное лицо 1')),
                        ('contact_employee2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contact_employee2', to='profiles.departmentstaff', verbose_name='Контактное лицо 2')),
                    ],
                    options={
                        'verbose_name': 'Дополнительное образование',
                        'verbose_name_plural': 'Дополнительное образование',
                        'db_table': 'pages_additionaleducation',
                    },
                ),
                migrations.CreateModel(
                    name='AdditionalEducationItem',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('title', models.CharField(max_length=255, verbose_name='Название программы')),
                        ('volume', models.CharField(help_text="Например, '72 академических часа' или '3 зачетные единицы'", max_length=100, verbose_name='Объем')),
                        ('study_mode', models.CharField(max_length=100, verbose_name='Форма обучения')),
                        ('language', models.CharField(max_length=100, verbose_name='Язык обучения')),
                        ('cost', models.DecimalField(decimal_places=2, help_text='Стоимость в рублях', max_digits=10, verbose_name='Стоимость')),
                        ('information', models.TextField(blank=True, verbose_name='Дополнительная информация')),
                        ('contact_person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contact_for_programs', to='profiles.departmentstaff', verbose_name='Контактное лицо')),
                        ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='academy.departmentinfo', verbose_name='Кафедра')),
                        ('program_director', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='directed_programs', to='profiles.departmentstaff', verbose_name='Руководитель программы')),
                        ('description', models.TextField(blank=True, null=True, verbose_name='Краткое описание')),
                    ],
                    options={
                        'verbose_name': 'Программа ДПО',
                        'verbose_name_plural': 'Программы ДПО',
                        'db_table': 'pages_additionaleducationitem',
                    },
                ),
            ],
            database_operations=[],
        ),
        move_content_type("pages", "profiledetails", "education", "profiledetails"),
        move_content_type("pages", "profile", "education", "profile"),
        move_content_type("pages", "studydirection", "education", "studydirection"),
        move_content_type("pages", "additionaleducation", "education", "additionaleducation"),
        move_content_type("pages", "additionaleducationitem", "education", "additionaleducationitem"),
    ]
