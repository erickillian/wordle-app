from django.urls import path
from rest_framework.routers import DefaultRouter
from ranker.wordle.views import WordleViewSet

from ranker.wordle import views

urlpatterns = [
    path('wordle/status', views.WordleStatus.as_view()),
    path('wordle/guess', views.WordleGuess.as_view()),
    path('wordle/today', views.WordlesToday.as_view()),
    path('wordle/shame', views.WordleWallOfShame.as_view()),
    path('wordle/leaders/guesses', views.WordleLeadersGuesses.as_view()),
    path('wordle/leaders/time', views.WordleLeadersTime.as_view()),
    path('wordle/stats', views.WordleStats.as_view()),
]

router = DefaultRouter()
router.register(r'wordle', WordleViewSet, basename='wordle')

urlpatterns += router.urls