
from rest_framework import serializers

from ranker.core.models import Player, Event, Match, RatingHistory
from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    username = serializers.CharField(required=True, write_only=True)
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    ("A user is already registered with this e-mail address."))
        return email

    def validate_username(self, username):
        email = get_adapter().clean_username(username)
        if allauth_settings.UNIQUE_EMAIL:
            if username and email_address_exists(email):
                raise serializers.ValidationError(
                    ("A user is already registered with this e-mail address."))
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(
                _("The two password fields didn't match."))
        return data

    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.save()
        return user

class PlayerSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    rating = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        source="playerrating.rating"
    )

    class Meta:
        model = Player
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Event
        fields = '__all__'


class RatingHistorySerializer(serializers.ModelSerializer):
    rating = serializers.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        model = RatingHistory
        exclude = ['id', 'player']


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'


class MatchHistorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    opponent_name = serializers.CharField(max_length=80)
    score = serializers.CharField(max_length=5)
    result = serializers.IntegerField()
    datetime = serializers.DateTimeField()
