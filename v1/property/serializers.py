from rest_framework.serializers import ModelSerializer
from v1.property.models import Property as PropertyModel, PropertyMedia


class PropertyMediaSerializer(ModelSerializer):
    class Meta:
        model = PropertyMedia
        fields = "__all__"


class PropertySerializer(ModelSerializer):
    extra_files = PropertyMediaSerializer(many=True)

    class Meta:
        model = PropertyModel
        fields = "__all__"

    def create(self, validated_data):
        extra_files = validated_data.pop("extra_files", [])
        property = PropertyModel.objects.create(**validated_data)
        for file in extra_files:
            PropertyMedia.objects.create(property=property, media=file)
        return property

    """def update(self, instance, validated_data):
        instance. = validated_data.pop("extra_files", [])
        for file in validated_data.extra_files:
            PropertyMedia.objects.create(property=property, media=file)
        return instance
"""