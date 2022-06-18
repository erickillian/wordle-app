from django.db.models import Avg, Count, Case, When
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import json

from ranker.wordle.constants.wordle import WORDLE_MAX_LENGTH, WORDLE_NUM_GUESSES

from ranker.core.models import (
    PlayerRating,
)
from ranker.core.serializers import (
    RatingHistorySerializer,
    MatchHistorySerializer,
)
from ranker.wordle.models import (
    Wordle,
)
from ranker.wordle.serializers import (
    WordleSerializer
)

from ranker.users.models import (
    Player,
)
from ranker.users.serializers import (
    PlayerSerializer
)
from ranker.core.services import data

class PlayerList(APIView):
    """
    List of all players
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        players = Player.objects.annotate(avg_guesses=Avg('wordle__guesses'))
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
            player = Player.objects.annotate(avg_guesses=Avg('wordle__guesses')).get(pk=player_id)
            serializer = PlayerSerializer(player)
            response = Response(serializer.data)
        except Player.DoesNotExist:
            response = Response(status=status.HTTP_404_NOT_FOUND)
        return response



class PlayerWordleStats(APIView):
    """
    Player history rating for charts
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, player_id):
        try:
            queryset = Player.objects.annotate(
                avg_guesses=Avg('wordle__guesses'), 
                avg_time=Avg('wordle__time'), 
                total_wordles=Count('wordle'),
                fails=Count(Case(When(wordle__fail=True, then=1)))
            ).get(pk=player_id)
            serializer = PlayerSerializer(queryset)
            return Response(serializer.data)
        except PlayerRating.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class PlayerWordleGuessDistribution(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, player_id):
        try:
            queryset = Wordle.objects.filter(player=player_id).values('guesses', 'fail').order_by('guesses')
            guess_distribution = {}

            for i in range(1, WORDLE_NUM_GUESSES+1):
                guess_distribution.setdefault(i, 0)

            for wordle in queryset:
                if not wordle['fail']:
                    guesses = wordle['guesses']
                    if guesses not in guess_distribution:
                        guess_distribution.setdefault(guesses, 1)
                    else:
                        guess_distribution[guesses] += 1

            response = {}
            response['labels'] = guess_distribution.keys()
            response['data'] = guess_distribution.values()

            return Response(response)
        except PlayerRating.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class PlayerWordles(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, player_id):
        try:
            queryset = Wordle.objects.filter(player=player_id).order_by('-date')
            serializer = WordleSerializer(queryset, many=True)
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