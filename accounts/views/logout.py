from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken


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
