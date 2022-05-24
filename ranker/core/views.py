from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ranker.core.models import (
    Player, Event, PlayerRating, DailyWordle, ActiveWordle,
)
from ranker.core.serializers import (
    PlayerSerializer,
    EventSerializer,
    RatingHistorySerializer,
    MatchHistorySerializer,
    ActiveWordleSerializer,
    WordleGuessSerializer
)
from ranker.core.services import data

import json, os, random
from ranker.settings.dev import BASE_DIR

import datetime

wordle_dictionary = json.load(open(os.path.join(BASE_DIR, 'ranker/core/constants/dictionary.json')))
wordle_target_words = json.load(open(os.path.join(BASE_DIR, 'ranker/core/constants/targetWords.json')))

from ranker.core.constants.wordle import WORDLE_MAX_LENGTH, WORDLE_NUM_GUESSES

N_LAST_MATCHES = 10
N_PLAYERS = 5
N_DAYS_STATS_MAIN = 7
LB_CACHE_MINUTES = 1

class LeaderBoard(APIView):
    """
    Get data for leaderboard. Data is cached for LB_CACHE_MINUTES
    minutes. Set it to 0 if you dont need any caching
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(LB_CACHE_MINUTES * 60, cache='leaderboard', key_prefix=''))
    def get(self, request):
        leaders = data.get_leaders(n_players=N_PLAYERS, rating_trend_days=N_DAYS_STATS_MAIN)
        # changes = data.get_changes_in_time(n_players=N_PLAYERS, n_days=N_DAYS_STATS_MAIN)
        maxes = data.get_maxes()
        totals = data.get_totals()

        return Response({
            'leaders': leaders,
            'weekly': [],
            'maxes': maxes,
            'totals': totals
        })


class PlayerList(APIView):
    """
    List of all players
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        players = Player.objects.all()
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data)


class PlayerDetail(APIView):
    """
    Player data
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, player_id):
        try:
            player = Player.objects.get(pk=player_id)
            serializer = PlayerSerializer(player)
            response = Response(serializer.data)
        except Player.DoesNotExist:
            response = Response(status=status.HTTP_404_NOT_FOUND)
        return response


class PlayerRatingHistory(APIView):
    """
    Player history rating for charts
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, player_id):
        try:
            player = PlayerRating.objects.get(pk=player_id)
            serializer = RatingHistorySerializer(player.rating_history_days, many=True)
            return Response(serializer.data)
        except PlayerRating.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class PlayerMatchHistory(APIView):
    """
    Player match history
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, player_id):
        summary = data.get_last_matches(player_id=player_id, n_matches=N_LAST_MATCHES)
        serializer = MatchHistorySerializer(summary, many=True)
        return Response(serializer.data)


class PlayerStats(APIView):
    """
    Simple player statistics
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, player_id):
        try:
            stats = data.get_player_stats(player_id=player_id)
            return Response(stats)
        except PlayerRating.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)



class Wordle(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            serializer = ActiveWordleSerializer(active_wordle)

            return JsonResponse(serializer.data)(player=request.user)
            # case where the player started a game and didnt finish
            serializer = ActiveWordleSerializer(active_wordle)

            return JsonResponse(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, guess):
        try:
            active_wordle = ActiveWordle.objects.get(player=request.user)
            wordle = DailyWordle.objects.get(player=request.user, date=datetime.date())

            serializer = WordleGuessSerializer(active_wordle)
            return JsonResponse(serializer.data)


            # case where the player started a game and didnt finish
            serializer = ActiveWordleSerializer(active_wordle)
            return JsonResponse(serializer.data)
        except ActiveWordle.DoesNotExist:
            word = random.choice(wordle_target_words)
            active_wordle = ActiveWordle.objects.create(player=request.user, word=word, guess_history=guess)

            return Response(status=status.HTTP_404_NOT_FOUND)
        except DailyWordle.DoesNotExist:
             return Response(status=status.HTTP_200_OK)


class WordleGuess(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    



class EventList(APIView):
    """
    List of all events
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


class EventDetail(APIView):
    """
    Detailed event information
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, response, event_id):
        try:
            event_details = data.get_event_details(event_id=event_id)
            response = Response(event_details)
        except Event.DoesNotExist:
            response = Response(status=status.HTTP_404_NOT_FOUND)
        return response
