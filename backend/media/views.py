from .models import Image
from rest_framework import viewsets
from .serializers import ImageSerializer
from .filters import ImageFilter
from .enums import ImageLocations
from rest_framework.response import Response


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    filterset_class = ImageFilter

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(file_location=ImageLocations.GAMES_IMG)

        return Response(serializer.data)
