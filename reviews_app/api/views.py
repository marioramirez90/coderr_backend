import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters

from reviews_app.models import Review
from .permissions import IsReviewerOrReadOnly
from .serializers import ReviewSerializer


class ReviewFilter(django_filters.FilterSet):
    business_user_id = django_filters.NumberFilter(field_name="business_user__id")
    reviewer_id = django_filters.NumberFilter(field_name="reviewer__id")

    class Meta:
        model = Review
        fields = ["business_user_id", "reviewer_id"]


class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ReviewFilter
    ordering_fields = ["updated_at", "rating"]

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsReviewerOrReadOnly]