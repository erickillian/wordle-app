from django.urls import path
from rest_framework.routers import DefaultRouter
from ranker.core.views import DailyWordleViewSet


from ranker.core import views

urlpatterns = [
    path('players/all', views.PlayerList.as_view()),
    path('players/leaderboard', views.LeaderBoard.as_view()),
    path('player/details/<int:player_id>', views.PlayerDetail.as_view()),
    path('player/stats/<int:player_id>', views.PlayerStats.as_view()),
    path('history/rating/<int:player_id>', views.PlayerRatingHistory.as_view()),
    path('history/match/<int:player_id>', views.PlayerMatchHistory.as_view()),
    path('wordle/status/', views.WordleStatus.as_view()),
    path('wordle/guess/', views.WordleGuess.as_view()),
    path('wordle/today/', views.WordlesToday.as_view()),
    # path('events/all', views.EventList.as_view()),
    # path('event/details/<int:event_id>', views.EventDetail.as_view())
]

router = DefaultRouter()
router.register(r'wordle', DailyWordleViewSet, basename='wordle')

urlpatterns += router.urls