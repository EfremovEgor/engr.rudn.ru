# Generated by Django 5.0.1 on 2024-02-13 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0040_departmentinfo_contact_employee_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='scientificcenters',
            name='page_url',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='Путь'),
        ),
    ]
