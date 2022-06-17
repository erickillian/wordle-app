
from numpy import require
from rest_framework import serializers
from ranker.wordle.constants.wordle import WORDLE_NUM_GUESSES

from ranker.wordle.models import Wordle

import json, os
from ranker.settings.dev import BASE_DIR

class ActiveWordleSerializer(serializers.Serializer):
    guesses = serializers.IntegerField()
    guess_history = serializers.CharField(max_length=30)
    solved = serializers.BooleanField()
    start_time = serializers.DateTimeField()
    correct = serializers.CharField(max_length=30)

    class Meta:
        exclude = ['word']

wordle_dictionary = json.load(open(os.path.join(BASE_DIR, 'ranker/wordle/constants/dictionary.json')))
def valid_guess(guess):
    if guess not in wordle_dictionary:
        raise serializers.ValidationError('Guess not a valid word')

def valid_num_guesses(guesses):
    if guesses > WORDLE_NUM_GUESSES:
        raise serializers.ValidationError('You have exceeded the number of allowed guesses')

class WordleGuessSerializer(serializers.Serializer):
    guess = serializers.CharField(max_length=5, validators=[valid_guess])

class WordleSerializer(serializers.ModelSerializer):
    player_name = serializers.CharField(source='player.full_name', read_only=True)
    time = serializers.DurationField()
    rank = serializers.IntegerField(required=False)
    class Meta:
        model = Wordle
        fields = '__all__'