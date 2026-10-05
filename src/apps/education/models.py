from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse

from apps.core.fields import RichTextField
from apps.core.models import PublishableModel


class StudyLevel(models.TextChoices):
    BACHELOR = "bachelor", "Бакалавриат"
    SPECIALIST = "specialist", "Специалитет"
    MASTER = "master", "Магистратура"
    POSTGRADUATE = "postgraduate", "Аспирантура"


class StudyLanguage(models.TextChoices):
    RU = "ru", "Русский"
    EN = "en", "Английский"


class StudyForm(models.TextChoices):
    FULL_TIME = "full_time", "Очная"
    PART_TIME = "part_time", "Очно-заочная"
    EXTRAMURAL = "extramural", "Заочная"


def default_languages():
    return [StudyLanguage.RU]


class StudyDirection(models.Model):
    name = models.CharField("Название", max_length=255)
    study_level = models.CharField("Уровень обучения", max_length=255, choices=StudyLevel.choices)
    cipher = models.CharField("Шифр", max_length=255)

    class Meta:
        verbose_name = "Направление подготовки"
        verbose_name_plural = "Направления подготовки"
        ordering = ["study_level", "cipher"]

    def __str__(self):
        return f"{self.cipher} {self.name}"


class Program(PublishableModel):
    """Профиль (образовательная программа) направления подготовки."""

    direction = models.ForeignKey(
        StudyDirection,
        verbose_name="Направление подготовки",
        on_delete=models.SET_NULL,
        related_name="programs",
        blank=True,
        null=True,
    )
    name = models.TextField("Название")
    cipher = models.CharField("Шифр", max_length=255, blank=True, null=True)
    study_level = models.CharField("Уровень обучения", max_length=255, choices=StudyLevel.choices)
    department = models.ForeignKey(
        "academy.Department",
        verbose_name="Кафедра / департамент",
        on_delete=models.SET_NULL,
        related_name="programs",
        blank=True,
        null=True,
    )
    languages = ArrayField(
        models.CharField("Язык обучения", max_length=255, choices=StudyLanguage.choices),
        verbose_name="Языки обучения",
        default=default_languages,
    )
    content = RichTextField("Описание программы")

    class Meta:
        verbose_name = "Образовательная программа"
        verbose_name_plural = "Образовательные программы"
        ordering = ["study_level", "cipher", "name"]

    def __str__(self):
        return f"{self.get_study_level_display()} — {self.name}"

    def get_absolute_url(self):
        return reverse("education:program_detail", args=[self.pk])

    @property
    def offers_list(self):
        order = {form: i for i, form in enumerate(StudyForm.values)}
        return sorted(self.offers.all(), key=lambda o: order.get(o.study_form, 99))


class ProgramOffer(models.Model):
    """Условия приёма по программе для конкретной формы обучения."""

    program = models.ForeignKey(
        Program,
        verbose_name="Программа",
        on_delete=models.CASCADE,
        related_name="offers",
        blank=True,
        null=True,
    )
    study_form = models.CharField(
        "Форма обучения", max_length=16, choices=StudyForm.choices, default=StudyForm.FULL_TIME
    )
    budget_places = models.PositiveIntegerField("Бюджетных мест", null=True, blank=True)
    paid_places = models.PositiveIntegerField("Платных мест", null=True, blank=True)
    study_duration = models.DecimalField(
        "Срок обучения, лет", max_digits=4, decimal_places=1, null=True, blank=True
    )
    price_first_year = models.PositiveIntegerField("1 год, ₽", null=True, blank=True)
    price_second_year = models.PositiveIntegerField("2 год, ₽", null=True, blank=True)
    price_third_year = models.PositiveIntegerField("3 год, ₽", null=True, blank=True)
    price_fourth_year = models.PositiveIntegerField("4 год, ₽", null=True, blank=True)
    price_fifth_year = models.PositiveIntegerField("5 год, ₽", null=True, blank=True)
    price_sixth_year = models.PositiveIntegerField("6 год, ₽", null=True, blank=True)
    admission_url = models.URLField("Ссылка на admission.rudn.ru", max_length=255, null=True, blank=True)
    note = RichTextField(
        "Примечание",
        blank=True,
        default="",
        help_text="Если заполнено, у количества бюджетных мест появится сноска «*».",
    )

    PRICE_FIELDS = (
        "price_first_year",
        "price_second_year",
        "price_third_year",
        "price_fourth_year",
        "price_fifth_year",
        "price_sixth_year",
    )

    class Meta:
        verbose_name = "Условия приёма"
        verbose_name_plural = "Условия приёма"
        ordering = ["program", "study_form"]
        constraints = [
            models.UniqueConstraint(fields=["program", "study_form"], name="education_offer_unique_form"),
        ]

    def __str__(self):
        if self.program_id:
            return f"{self.program.name} — {self.get_study_form_display()}"
        return f"Без программы — {self.get_study_form_display()}"

    @property
    def price_rows(self) -> list[dict]:
        """Стоимость по годам (до первого пустого года, не дольше срока обучения).

        Последняя строка выводится как «N-й год и далее».
        """
        prices = []
        for name in self.PRICE_FIELDS:
            value = getattr(self, name)
            if value is None:
                break
            prices.append(value)
        if self.study_duration:
            prices = prices[: max(int(self.study_duration), 1)]
        return [
            {"year": index + 1, "price": price, "last": index == len(prices) - 1}
            for index, price in enumerate(prices)
        ]

    @property
    def has_budget_scores(self) -> bool:
        return any(exam.score_budget for exam in self.exams.all())

    def exams_of_kind(self, kind):
        return [exam for exam in self.exams.all() if exam.kind == kind]

    @property
    def required_exams(self):
        return self.exams_of_kind(OfferExam.Kind.REQUIRED)

    @property
    def optional_exams(self):
        return self.exams_of_kind(OfferExam.Kind.OPTIONAL)


class ExamSubject(models.Model):
    name = models.CharField("Предмет", max_length=255)

    class Meta:
        verbose_name = "Вступительное испытание (предмет)"
        verbose_name_plural = "Вступительные испытания (предметы)"
        ordering = ["name"]

    def __str__(self):
        return self.name


class OfferExam(models.Model):
    class Kind(models.TextChoices):
        REQUIRED = "required", "Обязательный"
        OPTIONAL = "optional", "По выбору"

    offer = models.ForeignKey(ProgramOffer, on_delete=models.CASCADE, related_name="exams", verbose_name="Условия приёма")
    subject = models.ForeignKey(ExamSubject, on_delete=models.PROTECT, related_name="exams", verbose_name="Предмет")
    kind = models.CharField("Тип", max_length=16, choices=Kind.choices, default=Kind.REQUIRED)
    score_budget = models.CharField("Мин. балл (бюджет)", max_length=255, blank=True, default="")
    score_contract = models.CharField("Мин. балл (контракт)", max_length=255, blank=True, default="")
    position = models.PositiveIntegerField("Позиция", default=0)

    class Meta:
        verbose_name = "Минимальный балл"
        verbose_name_plural = "Минимальные баллы"
        ordering = ["-kind", "position", "id"]  # обязательные, затем по выбору

    def __str__(self):
        return f"{self.subject} — {self.score_budget or self.score_contract}"

    @property
    def contract_differs(self) -> bool:
        return bool(self.score_budget) and bool(self.score_contract) and self.score_budget != self.score_contract


class TranslatorModule(models.Model):
    """Настройки страницы «Модуль переводчика» (единственная запись)."""

    contact_employee1 = models.ForeignKey(
        "profiles.DepartmentStaff",
        verbose_name="Контактное лицо 1",
        related_name="+",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    contact_employee2 = models.ForeignKey(
        "profiles.DepartmentStaff",
        verbose_name="Контактное лицо 2",
        related_name="+",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = "Модуль переводчика"
        verbose_name_plural = "Модуль переводчика"

    def __str__(self):
        return "Модуль переводчика"

    def get_absolute_url(self):
        return reverse("education:translator_module")

    @property
    def contacts(self):
        return [c for c in (self.contact_employee1, self.contact_employee2) if c]


class AdditionalProgram(PublishableModel):
    title = models.CharField("Название программы", max_length=255)
    description = models.TextField("Краткое описание", blank=True, null=True)
    position = models.IntegerField("Позиция", default=0)
    department = models.ForeignKey(
        "academy.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Кафедра",
        related_name="additional_programs",
    )
    program_director = models.ForeignKey(
        "profiles.DepartmentStaff",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="directed_programs",
        verbose_name="Руководитель программы",
    )
    contact_person = models.ForeignKey(
        "profiles.DepartmentStaff",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contact_for_programs",
        verbose_name="Контактное лицо",
    )
    volume = models.CharField(
        "Объем", max_length=100, help_text="Например, «72 академических часа» или «3 зачетные единицы»"
    )
    study_mode = models.CharField("Форма обучения", max_length=100)
    language = models.CharField("Язык обучения", max_length=100)
    cost = models.DecimalField("Стоимость, ₽", max_digits=10, decimal_places=2)
    information = RichTextField("Дополнительная информация", blank=True)

    class Meta:
        verbose_name = "Программа ДПО"
        verbose_name_plural = "Программы ДПО"
        ordering = ["position", "title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("education:additional_program_detail", args=[self.pk])
