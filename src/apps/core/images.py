import io
from pathlib import Path

from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image, ImageOps


def fit_image_on_upload(field_file, size: tuple[int, int], quality: int = 85) -> None:
    """Обрезает и уменьшает только что загруженное изображение до пропорций `size`.

    Уже сохранённые файлы не трогаются (раньше картинка пережималась при каждом
    сохранении записи, теряя качество и плодя копии файлов).
    """
    if not field_file or getattr(field_file, "_committed", True):
        return
    try:
        image = Image.open(field_file)
        image = ImageOps.exif_transpose(image).convert("RGB")
    except Exception:
        return  # не изображение — пусть сработает валидация поля
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    buffer = io.BytesIO()
    image.save(buffer, "JPEG", quality=quality, optimize=True)
    buffer.seek(0)
    name = str(Path(field_file.name).with_suffix(".jpg").name)
    field_file.file = InMemoryUploadedFile(buffer, None, name, "image/jpeg", buffer.getbuffer().nbytes, None)
    field_file.name = name
