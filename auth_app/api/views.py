from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from auth_app.models import UserProfile
from .permissions import IsOwnerOrReadOnly
from .serializers import RegistrationSerializer, LoginSerializer,UserProfileSerializer

#endpiont........
class RegistrationView(generics.GenericAPIView):
    """Registrierung neu benutzer"""
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """legt Benutzer + Token"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "user_id": user.pk,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(generics.GenericAPIView):
    """Login alten benutzer."""
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "user_id": user.pk,
            },
            status=status.HTTP_200_OK,
        )
    
class ProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = "user__pk"
    lookup_url_kwarg = "pk"


class BusinessProfileListView(generics.ListAPIView):
    queryset = UserProfile.objects.filter(type="business")
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomerProfileListView(generics.ListAPIView):
    queryset = UserProfile.objects.filter(type="customer")
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]