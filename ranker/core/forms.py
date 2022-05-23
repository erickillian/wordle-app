from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.forms import UserCreationForm
from core.models import Player
from django.contrib.auth.forms import UserCreationForm

class MyCustomSignupForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Player
        fields = ('email','firstname','lastname', 'username')