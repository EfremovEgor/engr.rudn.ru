# Generated by Django 4.2.6 on 2024-01-28 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0007_profiledetails_sub_header'),
    ]

    operations = [
        migrations.AddField(
            model_name='profiledetails',
            name='paid_places',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Количество платных мест'),
        ),
        migrations.AlterField(
            model_name='profiledetails',
            name='budget_places',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Количество бюджетных мест'),
        ),
    ]