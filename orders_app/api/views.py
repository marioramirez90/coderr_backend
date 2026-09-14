from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from orders_app.models import Order
from .serializers import (
    OrderCreateSerializer,
    OrderSerializer,
    OrderUpdateStatusSerializer,
)


class OrderListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return (
            Order.objects.filter(
                Q(customer_user=user) | Q(business_user=user)
            ).order_by("-created_at")
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OrderCreateSerializer
        return OrderSerializer


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.request.method in ["PATCH", "PUT"]:
            return OrderUpdateStatusSerializer
        return OrderSerializer

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(
            Q(customer_user=user) | Q(business_user=user)
        )


class OrderCountView(APIView):
    """GET /api/order-count/{business_user_id}/ - Laufende Bestellungen"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, business_user_id):
        count = Order.objects.filter(
            business_user_id=business_user_id, status="in_progress"
        ).count()
        return Response({"order_count": count}, status=status.HTTP_200_OK)


class CompletedOrderCountView(APIView):
    """GET /api/completed-order-count/{business_user_id}/ - Abgeschlossene Bestellungen"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, business_user_id):
        count = Order.objects.filter(
            business_user_id=business_user_id, status="completed"
        ).count()
        return Response(
            {"completed_order_count": count}, status=status.HTTP_200_OK
        )