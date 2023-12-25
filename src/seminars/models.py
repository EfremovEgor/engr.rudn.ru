from django.db import models
from django.contrib.postgres.fields import ArrayField, DateRangeField
from django.contrib.admin.widgets import AdminDateWidget


class Seminar(models.Model):
    name = models.TextField(verbose_name="Название")
    department = models.TextField(verbose_name="БУП")
    date = DateRangeField(verbose_name="Даты проведения")

    holding_place = models.TextField("Место проведения")
    responsible_person = models.TextField("Ответственный за проведение(ФИО)")

    def __str__(self) -> str:
        return self.heading

    class Meta:
        verbose_name = "Научный семинар"
        verbose_name_plural = "Научные семинары"
