from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.utils import timezone
from django.forms.models import model_to_dict
from django.db.models import Avg, Count
from django.db.models.expressions import Window
from django.db.models.functions import RowNumber
from django.db.models import F


from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

import datetime

import json, os, random
from ranker.settings.dev import BASE_DIR

from ranker.wordle.models import (
    Wordle, ActiveWordle
)
from ranker.users.models import (
    Player,
)

from ranker.wordle.serializers import (
    ActiveWordleSerializer,
    WordleGuessSerializer,
    WordleSerializer,
)
from ranker.users.serializers import (
    PlayerSerializer,
)

from ranker.wordle.constants.wordle import WORDLE_MAX_LENGTH, WORDLE_NUM_GUESSES
wordle_target_words = json.load(open(os.path.join(BASE_DIR, 'ranker/wordle/constants/targetWords.json')))


def wordle_streak(player):
    """
    Returns how many days in a row a player has played (aka a players streak)
    """
    current_streak = 0
    streak_day = datetime.date.today()

    wordles = Wordle.objects.filter(player=player, date__lte = streak_day).values("date", "fail").order_by("-date")

    for wordle in wordles:
        date = wordle['date']
        fail = wordle['fail']

        if (not fail) and (date == streak_day):
            current_streak += 1
            streak_day -= datetime.timedelta(days=1)
        else:  # Awwww...
            break  # The current streak is done, exit the loop

    return current_streak



class WordleStatus(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            wordle = Wordle.objects.get(player=request.user, date=timezone.now().date())
            active_wordle = ActiveWordle.objects.get(player=request.user)
        except Wordle.DoesNotExist:
            try:
                active_wordle = ActiveWordle.objects.get(player=request.user)
                if active_wordle.date != timezone.now().date():
                    # If the user never completes their wordle for the day
                    active_wordle.delete()
                    active_wordle = ActiveWordle(word="?", guess_history="")
            except ActiveWordle.DoesNotExist:
                active_wordle = ActiveWordle(word="?", guess_history="")
        except ActiveWordle.DoesNotExist:
            # this should never happen, if it does there is a problem
            guess_history = "?"*WORDLE_MAX_LENGTH*(wordle.guesses-1)+wordle.word
            active_wordle = ActiveWordle(word=wordle.word, guess_history=guess_history)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ActiveWordleSerializer(active_wordle)
        return Response(serializer.data)

    


class WordleGuess(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = WordleGuessSerializer

    def post(self, request):
        active_wordles = ActiveWordle.objects.filter(player=request.user, start_time__date=timezone.now().date())
        daily_wordles = Wordle.objects.filter(player=request.user, date=timezone.now().date())

        if len(active_wordles) == 0 and len(daily_wordles) == 0:
            guess_serializer = WordleGuessSerializer(data=request.data)
            if guess_serializer.is_valid():
                # Deletes the old active wordle for the player if one exists
                active_wordles = ActiveWordle.objects.filter(player=request.user).delete()

                word = random.choice(wordle_target_words)
                active_wordle = ActiveWordle.objects.create(
                    player=request.user, 
                    guess_history=request.data['guess'], 
                    word=word
                )
                serializer = ActiveWordleSerializer(active_wordle)
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        # If an active wordle for the user exists and they have no wordles
        # on record for that day validate their guess 
        elif len(active_wordles) == 1 and len(daily_wordles) == 0:
            active_wordle = active_wordles[0]
            if active_wordle.guesses >= WORDLE_NUM_GUESSES:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            guess_serializer = WordleGuessSerializer(data=request.data)
            if guess_serializer.is_valid():
                active_wordle.guess_history += request.data['guess']
                active_wordle.save()
                serializer = ActiveWordleSerializer(active_wordle)
                
                if active_wordle.guesses == WORDLE_NUM_GUESSES or active_wordle.solved:
                    Wordle.objects.create(
                        player=request.user, 
                        word=active_wordle.word,
                        guesses=active_wordle.guesses,
                        date=active_wordle.date,
                        time=timezone.now()-active_wordle.start_time,
                        fail=not active_wordle.solved
                    )
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        elif len(active_wordles) == 1 and len(daily_wordles) == 1:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        elif len(active_wordles) > 1:
            active_wordles[0].delete()
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class WordleViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving Wordles.
    """
    def list(self, request):
        queryset = Wordle.objects.all()
        serializer = WordleSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Wordle.objects.all()
        daily_wordle = get_object_or_404(queryset, pk=pk)
        serializer = WordleSerializer(daily_wordle)
        return Response(serializer.data)

class WordlesToday(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = WordleSerializer

    def get(self, request):
        queryset = Wordle.objects.filter(
            date=timezone.now().date()
        ).order_by('fail', 'guesses', 'time').annotate(
            rank=Window(
                expression=RowNumber(),
                order_by=['fail', 'guesses', 'time']
            )
        )
        for obj in queryset:
            obj.streak = wordle_streak(obj.player)
            # print(streak, flush=True)

        serializer = WordleSerializer(queryset, many=True)
        return Response(serializer.data)

class WordleLeadersTime(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PlayerSerializer

    def get(self, request):

        queryset = Player.objects.annotate(avg_time=Avg('wordle__time'), total_wordles=Count('wordle')).filter(total_wordles__gte=10).order_by('avg_time')[:5]       
        serializer = PlayerSerializer(queryset, many=True)
        return Response(serializer.data)


class WordleLeadersGuesses(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PlayerSerializer

    def get(self, request):

        queryset = Player.objects.annotate(avg_guesses=Avg('wordle__guesses'), total_wordles=Count('wordle')).filter(total_wordles__gte=10).order_by('avg_guesses')[:5]
        for player in queryset:
            print(player, flush=True)
        serializer = PlayerSerializer(queryset, many=True)
        return Response(serializer.data)

class WordleStats(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PlayerSerializer

    def get(self, request):

        num_wordles = Wordle.objects.all().count()
        num_players = Player.objects.all().count()

        response = {}
        response['num_wordles'] = num_wordles
        response['num_players'] = num_players

        return Response(response)


class WordleWallOfShame(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = WordleSerializer

    def get(self, request):
        queryset = Wordle.objects.filter(fail=True)
        serializer = WordleSerializer(queryset, many=True)
        return Response(serializer.data)
