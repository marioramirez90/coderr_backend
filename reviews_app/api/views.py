"""
API views for the reviews app.

Provides endpoints for listing, creating, retrieving, updating, and deleting business reviews.
"""

import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions
from rest_framework.exceptions import PermissionDenied

from reviews_app.models import Review
from .permissions import IsCustomerUser, IsReviewerOrReadOnly
from .serializers import ReviewSerializer



class ReviewFilter(django_filters.FilterSet):
    business_user_id = django_filters.NumberFilter(
        field_name="business_user__id"
    )
    reviewer_id = django_filters.NumberFilter(field_name="reviewer__id")

    class Meta:
        model = Review
        fields = ["business_user_id", "reviewer_id"]


class ReviewListCreateView(generics.ListCreateAPIView):
    """GET /api/reviews/ & POST /api/reviews/."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ReviewFilter
    ordering_fields = ["updated_at", "rating"]

    def get_permissions(self):
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        business_user = serializer.validated_data["business_user"]
        if Review.objects.filter(
            reviewer=self.request.user, business_user=business_user
        ).exists():
            raise serializers.ValidationError(
                "A user can only submit one review per business profile."
            )
        serializer.save(reviewer=self.request.user)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET, PATCH, DELETE /api/reviews/{id}/."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsReviewerOrReadOnly]