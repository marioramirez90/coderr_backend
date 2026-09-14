from django.contrib.auth.models import User
from rest_framework import serializers

from offers_app.models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
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


class OfferCreateUpdateSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ["id", "title", "image", "description", "details"]

    def validate_details(self, value):
        if self.instance is None and len(value) != 3:
            raise serializers.ValidationError(
                "An offer must contain exactly 3 details."
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

        if details_data:
            for detail_data in details_data:
                offer_type = detail_data.get("offer_type")
                detail_obj = instance.details.filter(
                    offer_type=offer_type
                ).first()
                if detail_obj:
                    for key, val in detail_data.items():
                        setattr(detail_obj, key, val)
                    detail_obj.save()

        return instance