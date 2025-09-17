from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import api_view
from v1.property.models import Property
from v1.property.serializers import PropertySerializer, ListCreatePropertySerializer
from v1.property.permissions import IsAdminOrReadOnly
from v1.property.filters import PropertyQueryFilter


class ListAndCreatePropertyView(generics.ListCreateAPIView):
    queryset = Property.objects.all()
    serializer_class = ListCreatePropertySerializer
    search_fields = ["description", "benefits"]
    filterset_class = PropertyQueryFilter
    permission_classes = [IsAdminOrReadOnly]


class RetrieveOrUpdatePropertyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAdminOrReadOnly]
