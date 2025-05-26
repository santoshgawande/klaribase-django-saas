from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.serializers.token import CustomTokenObtainPairSerializer


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
