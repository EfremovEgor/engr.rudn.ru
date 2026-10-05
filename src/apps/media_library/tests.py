import shutil
import tempfile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from apps.news.models import NewsItem

from .models import MediaFile
from .services import find_usages

TMP_MEDIA = tempfile.mkdtemp()
PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde"
    b"\x00\x00\x00\x0cIDATx\x9cc\xf8\xcf\xc0\x00\x00\x03\x01\x01\x00\xc9\xfe\x92\xef\x00\x00\x00\x00IEND\xaeB`\x82"
)


@override_settings(MEDIA_ROOT=TMP_MEDIA)
class MediaLibraryTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TMP_MEDIA, ignore_errors=True)

    def setUp(self):
        self.user = User.objects.create_superuser("root", "root@example.com", "pass")
        self.client.force_login(self.user)

    def test_editor_upload_creates_media_file(self):
        response = self.client.post(
            reverse("media_library:editor_upload"),
            {"upload": SimpleUploadedFile("Фото Пример.png", PNG, content_type="image/png")},
        )
        self.assertEqual(response.status_code, 200)
        media = MediaFile.objects.get()
        self.assertEqual(response.json()["url"], media.url)
        self.assertEqual(media.kind, MediaFile.Kind.IMAGE)
        self.assertEqual((media.width, media.height), (1, 1))
        self.assertEqual(media.folder.name, "Загрузки из редактора")
        self.assertTrue(media.file.name.startswith("library/"))

    def test_dangerous_extension_rejected(self):
        response = self.client.post(
            reverse("media_library:upload"), {"file": SimpleUploadedFile("x.html", b"<script>", content_type="text/html")}
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(MediaFile.objects.exists())

    def test_upload_requires_staff(self):
        self.client.logout()
        response = self.client.post(reverse("media_library:upload"), {"file": SimpleUploadedFile("a.png", PNG)})
        self.assertEqual(response.status_code, 302)

    def test_picker_and_usages(self):
        self.client.post(reverse("media_library:upload"), {"file": SimpleUploadedFile("pic.png", PNG)})
        media = MediaFile.objects.get()
        data = self.client.get(reverse("media_library:picker"), {"kind": "image"}).json()
        self.assertEqual(data["total"], 1)
        self.assertEqual(find_usages(media), [])
        NewsItem.objects.create(title_ru="n", content_ru=f'<img src="{media.url}">')
        self.assertEqual(len(find_usages(media)), 1)
