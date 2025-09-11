import django_filters
from django.db import models
from v1.property.models import Property as PropertyModel


class PropertyQueryFilter(django_filters.FilterSet):
    price_base = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_roof = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    tag = django_filters.BaseInFilter(method="filter_tag")

    def filter_tag(self, queryset, name, values_list):
        tag_query_set = models.Q()
        for tag in values_list:
            tag_key, tag_value = tag.split(":", 1)
            tag_query_set &= models.Q(**{f"tags__{tag_key}": tag_value})

        return queryset.filter(tag_query_set)

    class Meta:
        model = PropertyModel
        fields = ["state", "lga", "type", "offer"]
