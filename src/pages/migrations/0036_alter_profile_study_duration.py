# Generated by Django 5.0.1 on 2024-02-11 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0035_remove_profiledetails_minimal_passing_scores_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='study_duration',
            field=models.FloatField(default=4, verbose_name='Длительность обучения'),
        ),
    ]