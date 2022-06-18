from rest_framework import serializers
from ranker.core.models import Event, Match, RatingHistory

class EventSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Event
        fields = '__all__'

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'


class MatchHistorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    opponent_name = serializers.CharField(max_length=80)
    score = serializers.CharField(max_length=5)
    result = serializers.IntegerField()
    datetime = serializers.DateTimeField()

class RatingHistorySerializer(serializers.ModelSerializer):
    rating = serializers.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        model = RatingHistory
        exclude = ['id', 'player']