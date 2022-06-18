
from numpy import require
from rest_framework import serializers
from ranker.wordle.constants.wordle import WORDLE_NUM_GUESSES

from ranker.users.models import Player, CustomAccountManager
from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
# from allauth.account.utils import setup_user_email
# from django.contrib.auth import get_user_model

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    username = serializers.CharField(required=True, write_only=True)
    firstname = serializers.CharField(required=True, write_only=True)
    lastname = serializers.CharField(required=True, write_only=True)
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
            'username': self.validated_data.get('username', ''),
            'firstname': self.validated_data.get('firstname', ''),
            'lastname': self.validated_data.get('lastname', ''),
            'password': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
        }

    def save(self, request):
        account_manager = CustomAccountManager
        cleaned_data = self.get_cleaned_data()
        user = account_manager.create_user(self, **cleaned_data)
        return user

class PlayerSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    avg_guesses = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    avg_time = serializers.DurationField(required=False)
    total_wordles = serializers.IntegerField(required=False)
    fails = serializers.IntegerField(required=False)
    class Meta:
        model = Player
        fields = ['full_name', 'id', 'avg_guesses', 'avg_time', 'total_wordles', 'fails', 'firstname', 'lastname']


