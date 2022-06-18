from django.urls import path
from rest_framework.routers import DefaultRouter
from ranker.core import views

urlpatterns = [
    path('players/leaderboard', views.LeaderBoard.as_view()),
]