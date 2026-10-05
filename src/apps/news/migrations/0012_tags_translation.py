# Тэги: вместо двух связей (tags / tags_en) на одну и ту же модель — одна связь и
# переводимое название тэга. Тэг, который использовался только в английских тэгах,
# становится тэгом только с английским названием.
from django.db import migrations, models

from apps.core.migration_utils import immediate_constraints


def split_tag_names(apps, schema_editor):
    Tag = apps.get_model("news", "Tag")
    NewsItem = apps.get_model("news", "NewsItem")
    ru_ids = set(NewsItem.tags.through.objects.values_list("tag_id", flat=True))
    en_ids = set(NewsItem.tags_en.through.objects.values_list("tag_id", flat=True))
    for tag in Tag.objects.all():
        only_en = tag.pk in en_ids and tag.pk not in ru_ids
        tag.name_ru = None if only_en else tag.name
        tag.name_en = tag.name if tag.pk in en_ids else None
        tag.save(update_fields=["name_ru", "name_en"])


def merge_tag_links(apps, schema_editor):
    NewsItem = apps.get_model("news", "NewsItem")
    RuThrough = NewsItem.tags.through
    EnThrough = NewsItem.tags_en.through
    existing = set(RuThrough.objects.values_list("newsitem_id", "tag_id"))
    RuThrough.objects.bulk_create(
        RuThrough(newsitem_id=news_id, tag_id=tag_id)
        for news_id, tag_id in EnThrough.objects.values_list("newsitem_id", "tag_id")
        if (news_id, tag_id) not in existing
    )


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0011_newsitem_tags_en_alter_newsitem_tags"),
    ]

    operations = [
        migrations.AddField(
            model_name="tag",
            name="name_ru",
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name="Тэг [ru]"),
        ),
        migrations.AddField(
            model_name="tag",
            name="name_en",
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name="Тэг [en]"),
        ),
        immediate_constraints(),
        migrations.RunPython(split_tag_names, migrations.RunPython.noop),
        immediate_constraints(),
        migrations.RunPython(merge_tag_links, migrations.RunPython.noop),
        migrations.RemoveField(model_name="newsitem", name="tags_en"),
        migrations.AlterField(
            model_name="newsitem",
            name="tags",
            field=models.ManyToManyField(blank=True, related_name="news_items", to="news.tag", verbose_name="Тэги"),
        ),
    ]
