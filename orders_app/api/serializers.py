"""
Serializers for the orders REST API endpoints.

Handles serialization and creation logic for customer orders and order status updates.
"""

from offers_app.models import OfferDetail
from rest_framework import serializers
from rest_framework.exceptions import NotFound

from orders_app.models import Order



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "created_at",
            "updated_at",
        ]


class OrderCreateSerializer(serializers.Serializer):
    offer_detail_id = serializers.IntegerField(write_only=True)

    def validate_offer_detail_id(self, value):
        try:
            detail = OfferDetail.objects.select_related("offer__user").get(
                id=value
            )
        except OfferDetail.DoesNotExist:
            raise NotFound("Offer detail not found.")
        return detail

    def create(self, validated_data):
        d = validated_data["offer_detail_id"]
        return Order.objects.create(
            customer_user=self.context["request"].user,
            business_user=d.offer.user,
            title=d.title,
            revisions=d.revisions,
            delivery_time_in_days=d.delivery_time_in_days,
            price=d.price,
            features=d.features,
            offer_type=d.offer_type,
            status="in_progress",
        )



class OrderUpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["status"]

    def to_internal_value(self, data):
        allowed_fields = {"status"}
        extra_fields = set(data.keys()) - allowed_fields
        if extra_fields:
            raise serializers.ValidationError(
                {field: "This field is not allowed." for field in extra_fields}
            )
        return super().to_internal_value(data)