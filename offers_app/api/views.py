"""
API views for the offers app.

Provides endpoints for listing, creating, retrieving, updating, and deleting offers,
retrieving single offer details, and fetching platform base information stats.
"""

import django_filters
from django.db.models import Avg, Min
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from offers_app.models import Offer, OfferDetail
from auth_app.models import UserProfile
from reviews_app.models import Review
from .permissions import IsBusinessUser, IsOwnerOrReadOnly
from .serializers import (
    OfferCreateUpdateSerializer,
    OfferDetailSerializer,
    OfferListDetailSerializer,
)


class StandardOfferPagination(PageNumberPagination):
    """Standard pagination for offers (10 items per page)."""

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class OfferFilter(django_filters.FilterSet):
    """Filter set for offer listing by creator_id, min_price, and max_delivery_time."""

    creator_id = django_filters.NumberFilter(field_name="user__id")
    min_price = django_filters.NumberFilter(
        field_name="details__price", lookup_expr="gte", distinct=True
    )
    max_delivery_time = django_filters.NumberFilter(
        field_name="details__delivery_time_in_days",
        lookup_expr="lte",
        distinct=True,
    )

    class Meta:
        model = Offer
        fields = ["creator_id", "min_price", "max_delivery_time"]


class OfferListCreateView(generics.ListCreateAPIView):
    """GET /api/offers/ & POST /api/offers/."""

    pagination_class = StandardOfferPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = OfferFilter
    search_fields = ["title", "description"]
    ordering_fields = ["updated_at", "min_price"]

    def get_queryset(self):
        return (
            Offer.objects.all()
            .annotate(min_price=Min("details__price"))
            .prefetch_related("details")
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OfferCreateUpdateSerializer
        return OfferListDetailSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), IsBusinessUser()]
        return [permissions.AllowAny()]


class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET /api/offers/{id}/, PATCH /api/offers/{id}/, DELETE /api/offers/{id}/."""

    queryset = Offer.objects.all().prefetch_related("details")
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ["PATCH", "PUT"]:
            return OfferCreateUpdateSerializer
        return OfferListDetailSerializer


class SingleOfferDetailView(generics.RetrieveAPIView):
    """GET /api/offerdetails/{id}/."""

    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


def _get_base_info_data():
    """Calculate platform statistics for base-info endpoint."""
    avg = Review.objects.aggregate(Avg("rating"))["rating__avg"]
    return {
        "review_count": Review.objects.count(),
        "average_rating": round(avg, 1) if avg is not None else 0.0,
        "business_profile_count": UserProfile.objects.filter(type="business").count(),
        "offer_count": Offer.objects.count(),
    }


class BaseInfoView(APIView):
    """GET /api/base-info/ - Overall platform statistics summary."""

    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response(_get_base_info_data(), status=status.HTTP_200_OK)
