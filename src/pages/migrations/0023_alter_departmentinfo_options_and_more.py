# Generated by Django 5.0.1 on 2024-02-08 19:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0022_alter_departmentinfo_options_departmentinfo_position'),
        ('profiles', '0012_alter_employeeprofile_office'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='departmentinfo',
            options={'ordering': ['position'], 'verbose_name': 'Департамен', 'verbose_name_plural': 'Департаменты'},
        ),
        migrations.AlterField(
            model_name='departmentinfo',
            name='head',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.employeeprofile', verbose_name='Руководитель'),
        ),
    ]
