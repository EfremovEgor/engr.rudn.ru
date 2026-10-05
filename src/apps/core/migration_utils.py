"""Вспомогательные операции для миграций реструктуризации.

Используются в миграциях, поэтому интерфейс этого модуля менять нельзя.
"""

from django.db import migrations
from django.db.models import F


def move_content_type(old_app: str, old_model: str, new_app: str, new_model: str):
    """Переносит ContentType (и права) модели в другое приложение/имя.

    Сохраняет назначенные группам права и историю изменений в админке.
    На пустой БД ничего не делает.
    """
    old_model, new_model = old_model.lower(), new_model.lower()

    def forwards(apps, schema_editor):
        ContentType = apps.get_model("contenttypes", "ContentType")
        Permission = apps.get_model("auth", "Permission")
        db = schema_editor.connection.alias
        ct = ContentType.objects.using(db).filter(app_label=old_app, model=old_model).first()
        if ct is None:
            return
        target = ContentType.objects.using(db).filter(app_label=new_app, model=new_model).first()
        if target is not None:
            # Уже создан post_migrate'ом (например, при повторном запуске) — переносим права на него.
            Permission.objects.using(db).filter(content_type=ct).update(content_type=target)
            ct.delete()
            ct = target
        else:
            ct.app_label = new_app
            ct.model = new_model
            ct.save(update_fields=["app_label", "model"])
        if old_model != new_model:
            for perm in Permission.objects.using(db).filter(content_type=ct):
                action, _, model = perm.codename.partition("_")
                if model == old_model:
                    new_codename = f"{action}_{new_model}"
                    if Permission.objects.using(db).filter(content_type=ct, codename=new_codename).exists():
                        continue
                    perm.codename = new_codename
                    perm.save(update_fields=["codename"])

    def backwards(apps, schema_editor):
        move_content_type(new_app, new_model, old_app, old_model).code(apps, schema_editor)

    return migrations.RunPython(forwards, backwards)


def copy_fields(app_label: str, model_name: str, mapping: dict[str, str]):
    """UPDATE model SET dst = src ... — копирует значения колонок одним запросом."""

    def forwards(apps, schema_editor):
        model = apps.get_model(app_label, model_name)
        model._base_manager.using(schema_editor.connection.alias).update(
            **{dst: F(src) for src, dst in mapping.items()}
        )

    return migrations.RunPython(forwards, migrations.RunPython.noop)


def immediate_constraints():
    """Проверять внешние ключи сразу, а не в конце транзакции.

    Ставится перед RunPython в миграциях, которые в той же транзакции меняют схему:
    иначе PostgreSQL отвечает «cannot CREATE INDEX ... because it has pending trigger events».
    """
    return migrations.RunSQL("SET CONSTRAINTS ALL IMMEDIATE", migrations.RunSQL.noop, elidable=True)
