from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import api_view
from v1.property.models import Property as PropertyModel
from v1.property.serializers import PropertySerializer
from v1.property.permissions import IsAuthenticatedOrReadOnly
from v1.property.filters import PropertyQueryFilter





class ListOrCreatePropertyView(generics.ListCreateAPIView):
    queryset = PropertyModel.objects.all()
    serializer_class = PropertySerializer
    search_fields = ["description", "benefits"]
    filterset_class = PropertyQueryFilter
    permission_classes = [IsAuthenticatedOrReadOnly]


class RetrieveOrUpdatePropertyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PropertyModel.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
