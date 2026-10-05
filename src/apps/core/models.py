from django.db import models


class PublishedQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)


class PublishableModel(models.Model):
    is_published = models.BooleanField(
        "Опубликовано",
        default=True,
        db_index=True,
        help_text="Снимите галочку, чтобы скрыть материал на сайте, не удаляя его.",
    )

    objects = PublishedQuerySet.as_manager()

    class Meta:
        abstract = True
