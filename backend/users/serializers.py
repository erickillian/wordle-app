from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
import requests


User = get_user_model()

profile_picture_prefix = "/static/profile_pictures/"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["slug", "display_name", "profile_picture"]

    def to_internal_value(self, data):
        if "profile_picture" in data:
            profile_picture = data["profile_picture"]
            if profile_picture.startswith(profile_picture_prefix):
                data["profile_picture"] = profile_picture[len(profile_picture_prefix) :]

        return super().to_internal_value(data)

    def to_representation(self, instance):
        if instance.profile_picture:
            instance.profile_picture = (
                f"{profile_picture_prefix}{instance.profile_picture}"
            )
        return super().to_representation(instance)


class UserSelfSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(max_length=100, allow_blank=True, required=False)
    email = serializers.EmailField(allow_blank=False, required=False, read_only=True)
    profile_picture = serializers.ChoiceField(choices=User.PROFILE_PICTURES, allow_blank=False, required=False)

    class Meta:
        model = User
        fields = ["slug", "email", "full_name", "date_joined", "color_mode", "profile_picture", "display_name"]
        read_only_fields = ["email", "date_joined", "slug", "display_name"]

    def to_internal_value(self, data):
        if "profile_picture" in data:
            profile_picture = data["profile_picture"]
            if profile_picture.startswith(profile_picture_prefix):
                data["profile_picture"] = profile_picture[len(profile_picture_prefix) :]
        return super().to_internal_value(data)

    def to_representation(self, instance):
        if instance.profile_picture:
            instance.profile_picture = (
                f"{profile_picture_prefix}{instance.profile_picture}"
            )
        return super().to_representation(instance)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password")


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    hcaptcha = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["email", "password", "hcaptcha"]

    def validate_hcaptcha(self, value):
        if not settings.HCAPTCHA_SECRET:
            return value

        response = requests.post(
            "https://api.hcaptcha.com/siteverify",
            data={
                "secret": settings.HCAPTCHA_SECRET,
                "response": value,
            },
        )
        if not response.json()["success"]:
            raise serializers.ValidationError("Invalid hCaptcha")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already in use")
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        email = validated_data["email"]
        password = validated_data["password"]
        user = User.objects.create_user(email=email, password=password)
        return user


class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class UserSessionSerializer(serializers.ModelSerializer):
    ip_address = serializers.CharField(source="metadata.ip_address", default="N/A")
    location = serializers.CharField(source="metadata.location", default="Unknown Location")
    device = serializers.CharField(source="metadata.device", default="Unknown Device")

    class Meta:
        model = OutstandingToken
        fields = ["created_at", "expires_at", "ip_address", "location", "device"]
