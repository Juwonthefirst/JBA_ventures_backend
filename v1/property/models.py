from django.db import models


def create_image_path(instance, filename):
    extension = filename.split(".")[-1]
    return f"{instance.pk}/base_image.{extension}"


class Property(models.Model):
    main_image = models.ImageField(upload_to=create_image_path)
    address = models.CharField(max_length=200)
    state = models.CharField(max_length=20)
    lga = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    type = models.CharField(max_length=50)
