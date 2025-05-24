from django.core.mail import send_mail
from django.urls import reverse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken

from accounts.models import CustomUser


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
            # from_email="gawandesantos@gmail.com",  # or Gmail will reject it
            from_email="noreply@klaribase.com",
            recipient_list=[user.email],
            fail_silently=False,
        )

        return Response(
            {"detail": "Password reset email sent."}, status=status.HTTP_200_OK
        )
