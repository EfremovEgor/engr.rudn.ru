from django.test import TestCase
from news.models import Tag, NewsItem


class TagTestCase(TestCase):
    def setUp(self):
        Tag.objects.create(name="Общая информация")

    def test_tag_creation(self):
        general_info = Tag.objects.get(name="Общая информация")
        self.assertTrue(isinstance(general_info, Tag))
        self.assertEqual(str(general_info), "Общая информация")


class NewsItemTestCase(TestCase):
    def setUp(self):
        tag = Tag.objects.create(name="Общая информация")
        instance = NewsItem.objects.create(
            title="Новый", preview_image=None, content="Новость"
        )
        instance.tags.add(tag)

    def test_animals_can_speak(self):
        general_info = NewsItem.objects.get(title="Новый")
        self.assertTrue(isinstance(general_info, NewsItem))
        self.assertEqual(str(general_info), "Новый")
