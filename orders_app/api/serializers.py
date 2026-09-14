from offers_app.models import OfferDetail
from rest_framework import serializers

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
            raise serializers.ValidationError("Angebotsdetail nicht gefunden.")
        return detail

    def create(self, validated_data):
        detail = validated_data["offer_detail_id"]
        customer = self.context["request"].user
        business = detail.offer.user

        return Order.objects.create(
            customer_user=customer,
            business_user=business,
            title=detail.title,
            revisions=detail.revisions,
            delivery_time_in_days=detail.delivery_time_in_days,
            price=detail.price,
            features=detail.features,
            offer_type=detail.offer_type,
            status="in_progress",
        )


class OrderUpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["status"]