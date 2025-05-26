from rest_framework import generics, status
from rest_framework.permissions import AllowAny

from accounts.models import CustomUser
from accounts.serializers.serializers import UserSerializer


class SignupView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
