# Generated by Django 5.0.1 on 2024-02-09 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0027_alter_scientificcenters_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='scientificcenters',
            name='position',
            field=models.IntegerField(default=1, verbose_name='Позиция'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='equipmentdata',
            name='purpose',
            field=models.TextField(verbose_name='Назначение'),
        ),
    ]