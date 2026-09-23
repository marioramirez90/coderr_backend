"""
API views for the authentication app.

Provides API endpoints for user registration, login authentication,
user profile retrieval/updating, and business/customer profile listings.
"""

from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from auth_app.models import UserProfile
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    LoginSerializer,
    RegistrationSerializer,
    UserProfileSerializer,
)


def _token_response(user, status_code):
    """Helper method to format token authentication response."""
    token, _ = Token.objects.get_or_create(user=user)
    payload = {
        "token": token.key,
        "username": user.username,
        "email": user.email,
        "user_id": user.pk,
    }
    return Response(payload, status=status_code)


class RegistrationView(generics.GenericAPIView):
    """User registration endpoint at POST /api/registration/."""

    serializer_class = RegistrationSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """Create new user account and return auth token."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return _token_response(user, status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    """User login endpoint at POST /api/login/."""

    serializer_class = LoginSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """Authenticate user credentials and return auth token."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        return _token_response(user, status.HTTP_200_OK)



class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """Retrieve or update user profile at GET /api/profile/{pk}/ and PATCH /api/profile/{pk}/."""

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = "user__pk"
    lookup_url_kwarg = "pk"


class BusinessProfileListView(generics.ListAPIView):
    """List business user profiles at GET /api/profiles/business/."""

    queryset = UserProfile.objects.filter(type="business")
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomerProfileListView(generics.ListAPIView):
    """List customer profiles at GET /api/profiles/customer/."""

    queryset = UserProfile.objects.filter(type="customer")
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]