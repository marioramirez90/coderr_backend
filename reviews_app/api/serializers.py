from rest_framework import serializers
from reviews_app.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.ReadOnlyField(source="reviewer.id")

    class Meta:
        model = Review
        fields = [
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "reviewer", "created_at", "updated_at"]

    def validate(self, attrs):
        request = self.context.get("request")
        business_user = attrs.get("business_user")

        # Verhindert, dass man sich selbst bewertet
        if request and request.user == business_user:
            raise serializers.ValidationError("Du kannst dich nicht selbst bewerten.")

        return attrs

    def create(self, validated_data):
        validated_data["reviewer"] = self.context["request"].user
        return super().create(validated_data)