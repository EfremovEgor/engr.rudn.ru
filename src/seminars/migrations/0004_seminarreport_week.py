# Generated by Django 5.0.1 on 2024-05-16 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seminars', '0003_alter_seminarreport_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='seminarreport',
            name='week',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Неделя'),
            preserve_default=False,
        ),
    ]