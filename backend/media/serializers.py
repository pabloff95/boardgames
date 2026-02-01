from rest_framework import serializers
from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return obj.file.url if obj.file else None

    class Meta:
        model = Image
        fields = ["id", "name", "url", "type"]
