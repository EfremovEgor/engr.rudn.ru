# Generated by Django 5.0.1 on 2024-02-09 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0029_partnerdata_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scientificcenters',
            name='equipment',
            field=models.ManyToManyField(blank=True, null=True, to='pages.equipmentdata', verbose_name='Оборудование'),
        ),
        migrations.AlterField(
            model_name='scientificcenters',
            name='partners',
            field=models.ManyToManyField(blank=True, null=True, to='pages.partnerdata', verbose_name='Сотрудничество, партнеры'),
        ),
    ]