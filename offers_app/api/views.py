import django_filters
from django.db.models import Avg, Min
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Offer, OfferDetail
from .permissions import IsBusinessUser, IsOwnerOrReadOnly
from .serializers import (
    OfferCreateUpdateSerializer,
    OfferDetailSerializer,
    OfferListDetailSerializer,
)

# Wichtig: Importiere Review aus deiner Review-App
# (Falls dein Ordner 'reviews' statt 'reviews_app' heißt, passe den Namen an)
from reviews_app.models import Review


# 1. Paginierung (10 Einträge pro Seite)
class StandardOfferPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


# 2. Filter für die Angebotsliste
class OfferFilter(django_filters.FilterSet):
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


# 3. GET /api/offers/ & POST /api/offers/
class OfferListCreateView(generics.ListCreateAPIView):
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


# 4. GET /api/offers/{id}/, PATCH /api/offers/{id}/, DELETE /api/offers/{id}/
class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all().prefetch_related("details")
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ["PATCH", "PUT"]:
            return OfferCreateUpdateSerializer
        return OfferListDetailSerializer


# 5. GET /api/offerdetails/{id}/
class SingleOfferDetailView(generics.RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


# 6. GET /api/base-info/
class BaseInfoView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        review_count = Review.objects.count()
        avg_rating_result = Review.objects.aggregate(Avg("rating"))[
            "rating__avg"
        ]
        average_rating = (
            round(avg_rating_result, 1)
            if avg_rating_result is not None
            else 0.0
        )
        offer_count = Offer.objects.count()

        data = {
            "review_count": review_count,
            "average_rating": average_rating,
            "offer_count": offer_count,
        }

        return Response(data, status=status.HTTP_200_OK)