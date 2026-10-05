"""Боковое меню админки, сгруппированное по задачам редактора."""

from django.urls import reverse

# Ссылки — готовые строки, а не функции: по строке unfold определяет активный пункт
# и не сворачивает группу меню при переходе внутрь раздела.


def _model(title, icon, label, permission="view"):
    app_label, model_name = label.split(".")
    return {
        "title": title,
        "icon": icon,
        "link": reverse(f"admin:{app_label}_{model_name}_changelist"),
        "permission": lambda request: request.user.has_perm(f"{app_label}.{permission}_{model_name}"),
    }


def _link(title, icon, url_name, permission=None, kwargs=None):
    return {
        "title": title,
        "icon": icon,
        "link": reverse(url_name, kwargs=kwargs),
        "permission": permission or (lambda request: request.user.is_staff),
    }


def sidebar_navigation(request):
    return [
        {
            "title": "Главное",
            "items": [
                _link("Панель управления", "dashboard", "admin:index"),
                _link("Переводы контента", "translate", "admin:translations_overview"),
                _model("Медиатека", "perm_media", "media_library.mediafile"),
            ],
        },
        {
            "title": "Материалы сайта",
            "collapsible": True,
            "items": [
                _model("Новости", "newspaper", "news.newsitem"),
                _model("Тэги новостей", "sell", "news.tag"),
                _model("Страницы", "article", "pages.page"),
                _model("Слайдер на главной", "view_carousel", "pages.mainslider"),
                _model("Контакты на главной", "contact_page", "pages.indexcontact"),
                _model("Документы", "description", "documents.document"),
            ],
        },
        {
            "title": "Образование",
            "collapsible": True,
            "items": [
                _model("Направления подготовки", "school", "education.studydirection"),
                _model("Образовательные программы", "menu_book", "education.program"),
                _model("Условия приёма", "assignment", "education.programoffer"),
                _model("Предметы испытаний", "quiz", "education.examsubject"),
                _model("Программы ДПО", "workspace_premium", "education.additionalprogram"),
                _model("Модуль переводчика", "record_voice_over", "education.translatormodule"),
            ],
        },
        {
            "title": "Академия и люди",
            "collapsible": True,
            "items": [
                _model("Кафедры", "apartment", "academy.department"),
                _model("Дирекция", "groups", "academy.administrationmember"),
                _model("Сотрудники", "badge", "profiles.employeeprofile"),
                _model("Сотрудники кафедр", "assignment_ind", "profiles.departmentstaff"),
                _model("Студенческий комитет", "diversity_3", "profiles.studentcommitteeprofile"),
            ],
        },
        {
            "title": "Наука",
            "collapsible": True,
            "items": [
                _model("Научные центры", "science", "science.scientificcenter"),
                _model("Научные семинары", "event", "seminars.seminar"),
                _model("Доклады", "co_present", "seminars.seminarreport"),
                _model("Докладчики", "mic", "seminars.seminarspeaker"),
                _model("Диссертационные советы", "gavel", "science.dissertationcommittee"),
                _model("Научные специальности", "biotech", "science.scientificspecialty"),
                _model("Оборудование", "precision_manufacturing", "science.equipment"),
                _model("Партнёры", "handshake", "science.partner"),
            ],
        },
        {
            "title": "Переводы и доступ",
            "collapsible": True,
            "items": [
                _link(
                    "Строки интерфейса (.po)",
                    "language",
                    "rosetta-file-list",
                    kwargs={"po_filter": "project"},
                    permission=lambda request: request.user.is_superuser
                    or request.user.groups.filter(name="translators").exists(),
                ),
                _model("Пользователи", "person", "auth.user"),
                _model("Группы и права", "group", "auth.group"),
            ],
        },
    ]
