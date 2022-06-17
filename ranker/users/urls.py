from django.urls import path
from ranker.users import views

urlpatterns = [
    # path('history/rating/<int:player_id>', views.PlayerRatingHistory.as_view()),
    # path('history/match/<int:player_id>', views.PlayerMatchHistory.as_view()),
    path('players/all', views.PlayerList.as_view()),
    path('player/details/<int:player_id>', views.PlayerDetail.as_view()),
    path('player/stats/<int:player_id>', views.PlayerStats.as_view()),
    path('player/<int:player_id>/wordles', views.PlayerWordles.as_view()),
    path('player/<int:player_id>/wordle/stats', views.PlayerWordleStats.as_view()),
    path('player/<int:player_id>/wordle/guess_distribution', views.PlayerWordleGuessDistribution.as_view()),
]
