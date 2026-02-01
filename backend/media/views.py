from .models import Image
from rest_framework import viewsets
from .serializers import ImageSerializer
from .filters import ImageFilter


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    filterset_class = ImageFilter
