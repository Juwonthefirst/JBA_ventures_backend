from django.http import QueryDict
from rest_framework import serializers
from v1.property.models import Property as PropertyModel, PropertyMedia
from v1.property.utils import process_image


class PropertyMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyMedia
        fields = ["id", "media"]


class ListCreatePropertySerializer(serializers.ModelSerializer):
    extra_media = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False
    )

    class Meta:
        model = PropertyModel
        fields = "__all__"
        extra_kwargs = {
            "address": {"write_only": True},
            "benefits": {"write_only": True},
            "type": {"write_only": True},
        }

    def create(self, validated_data):
        extra_media = validated_data.pop("extra_media", [])
        main_image = process_image(validated_data.pop("main_image"))
        property = PropertyModel.objects.create(**validated_data, main_image=main_image)
        for file in extra_media:
            file = process_image(file)
            PropertyMedia.objects.create(property=property, media=file)
        return property


class PropertySerializer(serializers.ModelSerializer):
    extra_media_upload = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False
    )
    removed_media_id = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )

    extra_media = PropertyMediaSerializer(many=True, read_only=True)

    class Meta:
        model = PropertyModel
        fields = [
            "main_image",
            "address",
            "state",
            "lga",
            "description",
            "benefits",
            "type",
            "offer",
            "price",
            "tags",
            "extra_media",
            "extra_media_upload",
            "removed_media_id",
        ]

    def to_internal_value(self, data):
        if isinstance(data, QueryDict):
            # data = data.copy()
            extra_media_upload = []
            benefits = []
            removed_media_id = []

            for key in data:
                if key.startswith("extra_media_upload["):
                    extra_media_upload.append(data.get(key))
                elif key.startswith("benefits["):
                    benefits.append(data.get(key))
                elif key.startswith("removed_media_id["):
                    removed_media_id.append(data.get(key))

            data.setlist("extra_media_upload", extra_media_upload)
            data.setlist("benefits", benefits)
            data.setlist("removed_media_id", removed_media_id)
        return super().to_internal_value(data)

    def update(self, instance, validated_data):
        extra_media = validated_data.pop("extra_media_upload", [])
        removed_media_id = validated_data.pop("removed_media_id", [])
        if removed_media_id:
            PropertyMedia.objects.filter(id__in=removed_media_id).delete()
        for file in extra_media:
            file = process_image(file)
            PropertyMedia.objects.create(property=instance, media=file)
        for key, value in validated_data.items():
            if key == "main_image":
                instance.main_image = process_image(value)

            elif hasattr(instance, key):
                setattr(instance, key, value)
        instance.save()
        return instance
