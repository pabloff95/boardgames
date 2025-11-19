from reviews.models import Review
from rest_framework import viewsets
from reviews.serializers import ReviewsSerializer
from django_filters.rest_framework import DjangoFilterBackend
from reviews.filters import ReviewFilter
from rest_framework.response import Response
from rest_framework.decorators import action


def get_reviews(self):
    reviews = Review.objects.all()

    serializer = self.get_serializer(reviews, many=True)
    return Response(serializer.data)


def get_filtered_reviews(self, filter):
    filtered_reviews = Review.objects.filter(**filter)

    serializer = self.get_serializer(filtered_reviews, many=True)
    return Response(serializer.data)
