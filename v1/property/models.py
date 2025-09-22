from django.db import models
from django.contrib.postgres.fields import ArrayField


def create_image_path(instance, filename):
    extension = filename.split(".")[-1]
    return f"{instance.pk}/base_image.{extension}"


def create_extra_media_path(instance, filename):
    return f"{instance.property.pk}/extra_media/{filename}"


class Property(models.Model):
    main_image = models.ImageField(upload_to=create_image_path)
    address = models.CharField(max_length=200)
    state = models.CharField(max_length=20)
    lga = models.CharField(max_length=50)
    description = models.TextField()
    benefits = ArrayField(models.CharField(max_length=150), default=list)
    type = models.CharField(max_length=50)
    offer = models.CharField(max_length=50)
    price = models.IntegerField()
    tags = models.JSONField(default=dict)

    class Meta:
        ordering = ["-id"]


class PropertyMedia(models.Model):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="extra_media"
    )
    media = models.FileField(upload_to=create_extra_media_path)
