from rest_framework.serializers import ModelSerializer
from v1.property.models import Property as PropertyModel


class PropertySerializer(ModelSerializer):
    class Meta:
        model = PropertyModel
        fields = "__all__"
