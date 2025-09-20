from os import read
from rest_framework import serializers
from v1.property.models import Property as PropertyModel, PropertyMedia


class PropertyMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyMedia
        fields = ["id", "media"]


class ListCreatePropertySerializer(serializers.ModelSerializer):
    extra_media = serializers.ListField(child=serializers.FileField(), write_only=True)

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
        property = PropertyModel.objects.create(**validated_data)
        for file in extra_media:
            PropertyMedia.objects.create(property=property, media=file)
        return property


class PropertySerializer(serializers.ModelSerializer):
    extra_media_upload = serializers.ListField(
        child=serializers.FileField(), write_only=True
    )
    extra_media = serializers.SerializerMethodField(read_only=True)

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
        ]

    def get_extra_media(self, obj):
        extra_media_object = obj.extra_media.values_list("media", flat=True)
        return [media.url for media in extra_media_object]

    def update(self, instance, validated_data):
        extra_media = validated_data.pop("extra_media_upload", [])
        for file in extra_media:
            PropertyMedia.objects.create(property=property, media=file)
        for key, value in validated_data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        instance.save()
        return instance
