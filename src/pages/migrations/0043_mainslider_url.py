# Generated by Django 5.0.1 on 2024-02-14 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0042_mainslider'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainslider',
            name='url',
            field=models.URLField(blank=True, max_length=255, null=True, verbose_name='Ссылка'),
        ),
    ]
