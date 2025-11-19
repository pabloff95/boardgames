from .models import Review
from rest_framework import viewsets
from .serializers import ReviewsSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ReviewFilter
from rest_framework.decorators import action
from .utils.get_reviews import get_filtered_reviews
from rest_framework.permissions import AllowAny


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter

    def get_permissions(self):
        if self.action in ["retrieve"]:
            return [AllowAny()]

        if self.action == "list" and "user" not in self.request.query_params:
            return [AllowAny()]

        return super().get_permissions()

    @action(detail=False, methods=["get"])
    def good_reviews(self, request):
        return get_filtered_reviews(self, filter={"score__gte": 4})

    @action(detail=False, methods=["get"])
    def bad_reviews(self, request):
        return get_filtered_reviews(self, filter={"score__lte": 2})
