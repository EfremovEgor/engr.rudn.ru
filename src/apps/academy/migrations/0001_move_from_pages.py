# Перенос моделей из приложения pages в academy.
# Только состояние Django: таблицы БД остаются прежними (db_table), данные не трогаются.
# ContentType и права переносятся, чтобы сохранить права групп и историю админки.

import django.db.models.deletion
from django.db import migrations, models

from apps.core.migration_utils import move_content_type


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0058_additionaleducationitem_description"),
        ("profiles", "0023_alter_employeeprofile_phone_numbers"),
        ("contenttypes", "0002_remove_content_type_name"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name='DepartmentInfo',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('name', models.TextField(verbose_name='Название департамента')),
                        ('info', models.TextField(verbose_name='Информация о департаменте')),
                        ('head', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='head_of_department', to='profiles.departmentstaff', verbose_name='Руководитель')),
                        ('position', models.IntegerField(verbose_name='Позиция')),
                        ('job_title', models.CharField(choices=[('director', 'Директор департамента'), ('head', 'Заведующий кафедрой')], default='director', max_length=32, verbose_name='Должность руководителя')),
                        ('staff', models.ManyToManyField(blank=True, to='profiles.departmentstaff', verbose_name='Сотрудники департамента')),
                        ('abbreviation', models.CharField(blank=True, max_length=255, null=True, verbose_name='Аббревиатура')),
                        ('contact_employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contact_employee', to='profiles.departmentstaff', verbose_name='Контактное лицо')),
                        ('info_en', models.TextField(blank=True, null=True, verbose_name='Информация о департаменте (англ.)')),
                        ('name_en', models.TextField(blank=True, null=True, verbose_name='Название департамента (англ.)')),
                    ],
                    options={
                        'ordering': ['position'],
                        'verbose_name': 'Департамент',
                        'verbose_name_plural': 'Департаменты',
                        'db_table': 'pages_departmentinfo',
                    },
                ),
                migrations.CreateModel(
                    name='AdministrationProfiles',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('position', models.PositiveIntegerField(verbose_name='Позиция')),
                        ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.employeeprofile', verbose_name='Сотрудник')),
                    ],
                    options={
                        'verbose_name': 'Профиль дирекции',
                        'verbose_name_plural': 'Профили дирекции',
                        'ordering': ['position', 'employee__full_name'],
                        'db_table': 'pages_administrationprofiles',
                    },
                ),
            ],
            database_operations=[],
        ),
        move_content_type("pages", "departmentinfo", "academy", "departmentinfo"),
        move_content_type("pages", "administrationprofiles", "academy", "administrationprofiles"),
    ]
