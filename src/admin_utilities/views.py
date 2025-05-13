from django.forms import model_to_dict
from django.shortcuts import get_object_or_404, render
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic.edit import FormView
from .forms import UpdateStudyProfilesForm
from pages.models import Profile, ProfileDetails, DepartmentInfo, StudyDirection
import csv
from django.utils.translation import gettext_lazy as _


class UpdateStudyProfilesView(FormView):
    form_class = UpdateStudyProfilesForm
    template_name = "admin_utilities/update_study_profiles.html"
    success_url = "/admin_utilities/update_study_profiles"

    def form_valid(self, form):
        text = (
            form.cleaned_data["data"]
            .read()
            .decode("utf-8-sig", errors="ignore")
            .splitlines()
        )
        StudyDirection.objects.all().delete()
        Profile.objects.all().delete()
        ProfileDetails.objects.all().delete()
        reader = csv.DictReader(text, delimiter=",")
        for item in reader:
            department = DepartmentInfo.objects.filter(
                abbreviation=item["Кафедра"].upper()
            ).first()
            direction = StudyDirection.objects.filter(
                cipher=item["Шифр Направления"]
            ).first()
            if direction is None:
                direction = StudyDirection(
                    name=item["Направление подготовки"],
                    cipher=item["Шифр Направления"],
                    study_level=item["Уровень обучения"],
                )
                direction.save()
            profile = Profile.objects.filter(
                name=item["Название профиля или специальности"],
            ).first()
            if profile is None:
                profile_cipher = item["Шифр специальности"] or None

                languages = []
                if item["Русский"] == "ИСТИНА" or item["Русский"] == "":
                    languages.append("ru")
                if item["Английский"] == "ИСТИНА":
                    languages.append("en")

                profile = Profile(
                    name=item["Название профиля или специальности"],
                    cipher=profile_cipher,
                    study_level=item["Уровень обучения"],
                    faculty_field=department,
                    language_fields=languages,
                    content="TBD",
                )
            budget_places = (
                int(item["Бюджетные места"]) if item["Бюджетные места"] else None
            )
            price_first_year = (
                int(item["Стоимость обучения по контракту(1 год)"])
                if item["Стоимость обучения по контракту(1 год)"].replace("–", "")
                else None
            )
            price_second_year = (
                int(item["Стоимость обучения по контракту(2 год)"])
                if item["Стоимость обучения по контракту(2 год)"].replace("–", "")
                else None
            )
            price_third_year = (
                int(item["Стоимость обучения по контракту(3 год)"])
                if item["Стоимость обучения по контракту(3 год)"].replace("–", "")
                else None
            )
            price_fourth_year = (
                int(item["Стоимость обучения по контракту(4 год)"])
                if item["Стоимость обучения по контракту(4 год)"].replace("–", "")
                else None
            )
            price_fifth_year = (
                int(item["Стоимость обучения по контракту(5 год)"])
                if item["Стоимость обучения по контракту(5 год)"].replace("–", "")
                else None
            )

            profile.save()
            required_subjects = {}
            optional_subjects = {}
            if sub := item["Обязательный предмет 1 (название)"]:
                required_subjects.update(
                    {sub: item["Обязательный предмет 1 (баллы бюджет или контракт)"]}
                )
            if sub := item["Обязательный предмет 2 (название)"]:
                required_subjects.update(
                    {sub: item["Обязательный предмет 2 (баллы бюджет или контракт)"]}
                )
            if sub := item["Обязательный предмет 3 (название)"]:
                required_subjects.update(
                    {sub: item["Обязательный предмет 3 (баллы бюджет или контракт)"]}
                )
            if sub := item["Обязательный предмет 4 (название)"]:
                required_subjects.update(
                    {sub: item["Обязательный предмет 4 (баллы бюджет или контракт)"]}
                )

            if sub := item["Дополнительный предмет 1 (название)"]:
                optional_subjects.update(
                    {sub: item["Дополнительный предмет 1 (баллы бюджет или контракт)"]}
                )
            if sub := item["Дополнительный предмет 2 (название)"]:
                optional_subjects.update(
                    {sub: item["Дополнительный предмет 2 (баллы бюджет или контракт)"]}
                )
            if sub := item["Дополнительный предмет 3 (название)"]:
                optional_subjects.update(
                    {sub: item["Дополнительный предмет 3 (баллы бюджет или контракт)"]}
                )
            if sub := item["Дополнительный предмет 4 (название)"]:
                optional_subjects.update(
                    {sub: item["Дополнительный предмет 4 (баллы бюджет или контракт)"]}
                )
            if sub := item["Дополнительный предмет 5 (название)"]:
                optional_subjects.update(
                    {sub: item["Дополнительный предмет 5 (баллы бюджет или контракт)"]}
                )
            minimal_passing_scores_budget = {
                "Обязательные предметы": [
                    {"subject": k, "score": v} for k, v in required_subjects.items()
                ],
                "Дополнительные предметы (один на выбор)": [
                    {"subject": k, "score": v} for k, v in optional_subjects.items()
                ],
            }

            required_subjects_contract = {}
            optional_subjects_contract = {}

            if sub := item["Обязательный предмет 1 (название)"]:
                if score := item[
                    "Обязательный предмет 1 (доп. баллы только для контракта)"
                ]:
                    required_subjects_contract.update({sub: score})
                else:
                    required_subjects_contract.update(
                        {
                            sub: item[
                                "Обязательный предмет 1 (баллы бюджет или контракт)"
                            ]
                        }
                    )
            if sub := item["Обязательный предмет 2 (название)"]:
                if score := item[
                    "Обязательный предмет 2 (доп. баллы только для контракта)"
                ]:
                    required_subjects_contract.update({sub: score})
                else:
                    required_subjects_contract.update(
                        {
                            sub: item[
                                "Обязательный предмет 2 (баллы бюджет или контракт)"
                            ]
                        }
                    )
            if sub := item["Обязательный предмет 3 (название)"]:
                if score := item[
                    "Обязательный предмет 3 (доп. баллы только для контракта)"
                ]:
                    required_subjects_contract.update({sub: score})
                else:
                    required_subjects_contract.update(
                        {
                            sub: item[
                                "Обязательный предмет 3 (баллы бюджет или контракт)"
                            ]
                        }
                    )
            if sub := item["Обязательный предмет 4 (название)"]:
                if score := item[
                    "Обязательный предмет 4 (доп. баллы только для контракта)"
                ]:
                    required_subjects_contract.update({sub: score})
                else:
                    required_subjects_contract.update(
                        {
                            sub: item[
                                "Обязательный предмет 4 (баллы бюджет или контракт)"
                            ]
                        }
                    )

            if sub := item["Дополнительный предмет 1 (название)"]:
                if score := item[
                    "Дополнительный предмет 1 (доп. баллы только для контракта)"
                ]:
                    optional_subjects_contract.update({sub: score})
                else:
                    optional_subjects_contract.update(
                        {
                            sub: item[
                                "Дополнительный предмет 1 (баллы бюджет или контракт)"
                            ]
                        }
                    )
            if sub := item["Дополнительный предмет 2 (название)"]:
                if score := item[
                    "Дополнительный предмет 2 (доп. баллы только для контракта)"
                ]:
                    optional_subjects_contract.update({sub: score})
                else:
                    optional_subjects_contract.update(
                        {
                            sub: item[
                                "Дополнительный предмет 2 (баллы бюджет или контракт)"
                            ]
                        }
                    )
            if sub := item["Дополнительный предмет 3 (название)"]:
                if score := item[
                    "Дополнительный предмет 3 (доп. баллы только для контракта)"
                ]:
                    optional_subjects_contract.update({sub: score})
                else:
                    optional_subjects_contract.update(
                        {
                            sub: item[
                                "Дополнительный предмет 3 (баллы бюджет или контракт)"
                            ]
                        }
                    )
            if sub := item["Дополнительный предмет 4 (название)"]:
                if score := item[
                    "Дополнительный предмет 4 (доп. баллы только для контракта)"
                ]:
                    optional_subjects_contract.update({sub: score})
                else:
                    optional_subjects_contract.update(
                        {
                            sub: item[
                                "Дополнительный предмет 4 (баллы бюджет или контракт)"
                            ]
                        }
                    )
            if sub := item["Дополнительный предмет 5 (название)"]:
                if score := item[
                    "Дополнительный предмет 5 (доп. баллы только для контракта)"
                ]:
                    optional_subjects_contract.update({sub: score})
                else:
                    optional_subjects_contract.update(
                        {
                            sub: item[
                                "Дополнительный предмет 5 (баллы бюджет или контракт)"
                            ]
                        }
                    )
            if not budget_places:
                minimal_passing_scores_budget = None
            minimal_passing_scores_contract = {
                "Обязательные предметы": [
                    {"subject": k, "score": v}
                    for k, v in required_subjects_contract.items()
                ],
                "Дополнительные предметы (один на выбор)": [
                    {"subject": k, "score": v}
                    for k, v in optional_subjects_contract.items()
                ],
            }

            details = ProfileDetails(
                name=f'{item["Уровень обучения"]} {item["Форма обучениия"].capitalize()} {item["Название профиля или специальности"]}',
                budget_places=budget_places,
                price_first_year=price_first_year,
                price_second_year=price_second_year,
                price_third_year=price_third_year,
                price_fourth_year=price_fourth_year,
                price_fifth_year=price_fifth_year,
                minimal_passing_scores_budget=minimal_passing_scores_budget,
                minimal_passing_scores_contract=minimal_passing_scores_contract,
                study_duration=float(item["Продолжительность обучения, лет"]),
                admission_url=item["Ссылка на страницу на сайте admission.rudn.ru"],
            )
            study_type = item["Форма обучениия"]
            if item["Название профиля или специальности"] == "Архитектура":
                print(study_type)
                print(budget_places)
            details.save()
            if study_type == "очная":
                profile.full_time_details = details
            if study_type == "очно-заочная":
                profile.part_time_details = details
            if study_type == "заочная":
                profile.extramural_details = details
            profile.save()
            direction.profiles.add(profile)
            direction.save()
        return super().form_valid(form)
