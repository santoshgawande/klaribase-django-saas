from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from django.urls import reverse
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken

from .models import CustomUser
from .serializers import LoginSerializer, UserSerializer


class SignupView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("Received logout request")
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"detail": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            print("✅ Token blacklisted successfully")
            return Response(
                {"detail": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT
            )

        except TokenError as e:
            print("TokenError:", str(e))
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("General Exception:", str(e))
            return Response(
                {"detail": "Unexpected error: " + str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not user.check_password(old_password):
            return Response({"detail": "Old password is incorrect"}, status=400)

        try:
            validate_password(new_password, user)
        except Exception as e:
            return Response({"detail": list(e)}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response(
            {"detail": "Password updated Successfully."}, status=status.HTTP_200_OK
        )


class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response(
                {"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Create a time-limited token (JWT)
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)

        # Example reset URL
        reset_url = (
            request.build_absolute_uri(reverse("reset-password")) + f"?token={token}"
        )

        # send email
        send_mail(
            subject="Klaribase Password Reset",
            message=f"Hi {user.username},\n\nClick to reset your password: {reset_url}",
            from_email="noreply@klaribase.com",
            recipient_list=[email],
            fail_silently=False,
        )

        return Response(
            {"detail": "Password reset email sent."}, status=status.HTTP_200_OK
        )


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
