from .models import Review
from rest_framework import viewsets
from .serializers import ReviewsSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ReviewFilter
from rest_framework.response import Response
from rest_framework.decorators import action


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter

    @action(detail=False, methods=["get"])
    def good_reviews(self, request):
        good_reviews = Review.objects.filter(score__gte=4)

        serializer = self.get_serializer(good_reviews, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def bad_reviews(self, request):
        bad_reviews = Review.objects.filter(score__lte=2)

        serializer = self.get_serializer(bad_reviews, many=True)
        return Response(serializer.data)
