from django.contrib.auth.hashers import make_password
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken

from accounts.models import CustomUser


class ResetPasswordView(APIView):
    def post(self, request):
        token = request.data.get("token")
        new_password = request.data.get("password")

        try:
            validated_token = UntypedToken(token)
            user_id = validated_token["user_id"]
            user = CustomUser.object.get(id=user_id)
        except (TokenError, CustomUser.DoesNotExist):
            return Response(
                {"detail": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.password = make_password(new_password)
        user.save()
        return Response(
            {"detail": "Password has been reset."}, status=status.HTTP_200_OK
        )
