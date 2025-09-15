from rest_framework import serializers
from v1.property.models import Property as PropertyModel, PropertyMedia


class PropertyMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyMedia
        fields = ["id", "media"]
        


class PropertySerializer(serializers.ModelSerializer):
    extra_media = serializers.ListField(child=serializers.FileField())
    
    class Meta:
        model = PropertyModel
        fields = "__all__"

    def create(self, validated_data):
     
        extra_media = validated_data.pop("extra_media_upload", [])
        property = PropertyModel.objects.create(**validated_data)
        for file in extra_media:
            PropertyMedia.objects.create(property=property, media=file)
        return property

    """def update(self, instance, validated_data):
        instance. = validated_data.pop("extra_media", [])
        for file in validated_data.extra_media:
            PropertyMedia.objects.create(property=property, media=file)
        return instance
"""
