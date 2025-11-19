from .models import Review
from rest_framework import viewsets
from .serializers import ReviewsSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ReviewFilter
from rest_framework.response import Response
from rest_framework.decorators import action
from .utils.get_data import get_reviews, get_filtered_reviews


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter

    def get(self, request):
        return get_reviews(self)

    @action(detail=False, methods=["get"])
    def good_reviews(self, request):
        return get_filtered_reviews(self, filter={"score__gte": 4})

    @action(detail=False, methods=["get"])
    def bad_reviews(self, request):
        return get_filtered_reviews(self, filter={"score__lte": 2})
