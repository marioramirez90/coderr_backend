"""
API views for the orders app.

Provides endpoints for listing/creating orders, retrieving/updating/deleting order details,
and counting active or completed orders for a business profile.
"""

from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from orders_app.models import Order
from .permissions import IsCustomerUser, IsOrderBusinessUser
from .serializers import (
    OrderCreateSerializer,
    OrderSerializer,
    OrderUpdateStatusSerializer,
)


class OrderListCreateView(generics.ListCreateAPIView):
    """GET /api/orders/ & POST /api/orders/."""

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), IsCustomerUser()]
        return [permissions.IsAuthenticated()]

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET, PATCH, DELETE /api/orders/{id}/."""

    queryset = Order.objects.all()

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [permissions.IsAdminUser()]
        if self.request.method in ["PATCH", "PUT"]:
            return [permissions.IsAuthenticated(), IsOrderBusinessUser()]
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method in ["PATCH", "PUT"]:
            return OrderUpdateStatusSerializer
        return OrderSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(OrderSerializer(instance).data, status=status.HTTP_200_OK)



class OrderCountView(APIView):
    """GET /api/order-count/{business_user_id}/ - Ongoing in-progress orders count."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, business_user_id):
        get_object_or_404(User, id=business_user_id, profile__type="business")
        count = Order.objects.filter(
            business_user_id=business_user_id, status="in_progress"
        ).count()
        return Response({"order_count": count}, status=status.HTTP_200_OK)


class CompletedOrderCountView(APIView):
    """GET /api/completed-order-count/{business_user_id}/ - Completed orders count."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, business_user_id):
        get_object_or_404(User, id=business_user_id, profile__type="business")
        count = Order.objects.filter(
            business_user_id=business_user_id, status="completed"
        ).count()
        return Response(
            {"completed_order_count": count}, status=status.HTTP_200_OK
        )