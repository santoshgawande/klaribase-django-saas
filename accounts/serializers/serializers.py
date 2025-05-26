from django.contrib.auth import authenticate
from rest_framework import serializers

from accounts.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "password", "role"]

    def create(self, validated_data):
        return CustomUser.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            password=validated_data["password"],
            role=validated_data.get("role", "member"),
        )


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data["email"], password=data["password"])
        if user is None:
            raise serializers.ValidationError("Invalid email or password.")
        if not user.is_active:
            return serializers.ValidationError("User account is disabled.")
        data["user"] = user
        return data
