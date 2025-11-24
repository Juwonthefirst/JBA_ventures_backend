from io import BytesIO
from traceback import print_stack
from PIL import Image
from django.core.files.base import ContentFile


def process_image(image_file):
    try:
        img = Image.open(image_file)

        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGB")

        img.thumbnail((600, 600), Image.Resampling.LANCZOS)
        buffer = BytesIO()
        img.save(buffer, format="WEBP", quality=85, method=6)

        (file_name, _) = image_file.name.rsplit(".", 1)
        buffer.seek(0)
        return ContentFile(buffer.read(), name=".".join([file_name, "webp"]))
    except Exception as e:
        print_stack(e)
        return image_file
