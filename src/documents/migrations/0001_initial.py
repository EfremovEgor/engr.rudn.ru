# Generated by Django 4.2.6 on 2024-01-26 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicantsCISNormativeDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('file', models.FileField(upload_to='documents', verbose_name='Файл')),
            ],
            options={
                'verbose_name': 'Ссылка на нормативный документ для граждан российской федерации и стран снг',
                'verbose_name_plural': 'Ссылки на нормативные документы для граждан российской федерации и стран снг',
            },
        ),
        migrations.CreateModel(
            name='ApplicantsForeignNormativeDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('file', models.FileField(upload_to='documents', verbose_name='Файл')),
            ],
            options={
                'verbose_name': 'Ссылка на нормативный документ для иностранных граждан',
                'verbose_name_plural': 'Ссылки на нормативные документы для иностранных граждан',
            },
        ),
    ]