# Generated by Django 4.2.6 on 2024-01-26 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0003_studentsapplications_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentsapplications',
            name='position',
            field=models.IntegerField(default=1, verbose_name='Позиция'),
            preserve_default=False,
        ),
    ]
