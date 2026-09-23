"""
Serializers for the offers REST API endpoints.

Handles serialization, nested serialization, and validation for offers and offer details.
"""

from django.contrib.auth.models import User
from rest_framework import serializers

from offers_app.models import Offer, OfferDetail



class OfferDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField(required=False)
    revisions = serializers.IntegerField(required=False, min_value=0)
    delivery_time_in_days = serializers.IntegerField(required=False, min_value=1)
    price = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, min_value=0
    )
    features = serializers.JSONField(required=False)
    offer_type = serializers.CharField(required=False)

    class Meta:
        model = OfferDetail
        fields = [
            "id",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
        ]

    def to_internal_value(self, data):
        allowed_fields = {
            "id",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
        }
        extra_fields = set(data.keys()) - allowed_fields
        if extra_fields:
            raise serializers.ValidationError(
                {field: "This field is not allowed." for field in extra_fields}
            )
        return super().to_internal_value(data)


class OfferDetailLinkSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ["id", "url"]

    def get_url(self, obj):
        return f"/offerdetails/{obj.id}/"


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username"]


class OfferListDetailSerializer(serializers.ModelSerializer):
    details = OfferDetailLinkSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = UserDetailsSerializer(source="user", read_only=True)

    class Meta:
        model = Offer
        fields = [
            "id",
            "user",
            "title",
            "image",
            "description",
            "created_at",
            "updated_at",
            "details",
            "min_price",
            "min_delivery_time",
            "user_details",
        ]

    def get_min_price(self, obj):
        prices = [d.price for d in obj.details.all()]
        return min(prices) if prices else 0

    def get_min_delivery_time(self, obj):
        times = [d.delivery_time_in_days for d in obj.details.all()]
        return min(times) if times else 0


def _update_offer_details(instance, details_data):
    """Helper function to update associated OfferDetail instances."""
    if not details_data:
        return
    for detail_data in details_data:
        offer_type = detail_data.get("offer_type")
        detail_obj = instance.details.filter(offer_type=offer_type).first()
        if detail_obj:
            for key, val in detail_data.items():
                if key != "id":
                    setattr(detail_obj, key, val)
            detail_obj.save()


class OfferCreateUpdateSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True, required=False)

    class Meta:
        model = Offer
        fields = ["id", "title", "image", "description", "details"]

    def to_internal_value(self, data):
        allowed_fields = {"title", "image", "description", "details"}
        extra_fields = set(data.keys()) - allowed_fields
        if extra_fields:
            raise serializers.ValidationError(
                {field: "This field is not allowed." for field in extra_fields}
            )
        return super().to_internal_value(data)

    def validate_details(self, value):
        if self.instance is None and len(value) != 3:
            raise serializers.ValidationError(
                "An offer must contain exactly 3 details."
            )
        valid_types = {"basic", "standard", "premium"}
        existing_types = (
            set(self.instance.details.values_list("offer_type", flat=True))
            if self.instance
            else valid_types
        )
        for detail in value:
            offer_type = detail.get("offer_type")
            if not offer_type or offer_type not in valid_types:
                raise serializers.ValidationError(
                    "Each detail must contain a valid offer_type ('basic', 'standard', or 'premium')."
                )
            if self.instance and offer_type not in existing_types:
                raise serializers.ValidationError(
                    f"Detail offer_type '{offer_type}' does not exist on this offer."
                )
        return value

    def create(self, validated_data):
        details_data = validated_data.pop("details")
        user = self.context["request"].user
        offer = Offer.objects.create(user=user, **validated_data)
        for detail in details_data:
            OfferDetail.objects.create(offer=offer, **detail)
        return offer

    def update(self, instance, validated_data):
        details_data = validated_data.pop("details", None)
        instance.title = validated_data.get("title", instance.title)
        instance.image = validated_data.get("image", instance.image)
        instance.description = validated_data.get(
            "description", instance.description
        )
        instance.save()
        _update_offer_details(instance, details_data)
        return instance