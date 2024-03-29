# Generated by Django 5.0.1 on 2024-02-08 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0021_departmentinfo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='departmentinfo',
            options={'ordering': ['name'], 'verbose_name': 'Департамен', 'verbose_name_plural': 'Департаменты'},
        ),
        migrations.AddField(
            model_name='departmentinfo',
            name='position',
            field=models.IntegerField(default=1, verbose_name='Позиция'),
            preserve_default=False,
        ),
    ]
