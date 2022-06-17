from django.contrib import admin

from .models import Wordle, ActiveWordle

admin.site.register([Wordle, ActiveWordle])
