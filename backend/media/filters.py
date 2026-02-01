import django_filters
from .models import Image


class ImageFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    type = django_filters.CharFilter(field_name="type", lookup_expr="exact")

    class Meta:
        model = Image
        fields = ["id", "name", "type"]
