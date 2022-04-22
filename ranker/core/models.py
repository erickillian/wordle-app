from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.utils import timezone

from django.contrib.auth.models import AbstractUser

from ranker.core.rankings import EloRating
import json


class User(AbstractUser):
    # phone = models.CharField(
    #     verbose_name=_('phone number'), max_length=40, null=True, blank=True
    # )

    class Meta:
        db_table = 'user'

class Player(models.Model):
    """Table for keeping player information."""
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)

    class Meta:
        unique_together = ('first_name', 'last_name',)

    def __str__(self):
        """Display player's full name as string object representation."""
        return self.full_name

    @property
    def full_name(self):
        """The players full name, first plus last name."""
        full_name = f'{self.first_name} {self.last_name}'
        return full_name

    class Meta:
        db_table = 'player'
        verbose_name = ('player')
        verbose_name_plural = ('players')


class Match(models.Model):
    """Table for keeping track of game scores and winners."""
    winner = models.ForeignKey(Player, default=None, related_name='won_matches',on_delete=models.CASCADE)
    winning_score = models.IntegerField(default=None)
    loser = models.ForeignKey(Player, default=None, related_name='lost_matches', on_delete=models.CASCADE)
    losing_score = models.IntegerField(default=None)
    datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """Display match description as string object representation."""
        return self.description

    @staticmethod
    def get_recent_matches(num_matches: int):
        """Get specified number of recent matches in descending date."""
        recent_matches = Match.objects.all().order_by('-datetime')
        if recent_matches is not None:
            recent_matches = recent_matches[0:num_matches]
        return recent_matches

    @property
    def score(self):
        """Hyphenated version of match score, i.e. 21-19"""
        score = f'{self.winning_score}-{self.losing_score}'
        return score

    @property
    def date(self):
        """Date part of match datetime."""
        date = self.datetime.strftime('%m/%d/%Y')
        return date
    
    @property
    def description(self):
        """Description of who defeated who and what the score was."""
        description = (
            f'{self.date}: {self.winner} defeated {self.loser} {self.score}'
        )
        return description

    def save(self, *args, **kwargs):
        if self.id:  # occurs when the match already exists and is being updated
            super().save(*args, **kwargs)
            PlayerRating.generate_ratings()
        else:  # occurs when it's a new match being added
            super().save(*args, **kwargs)
            elo_rating = EloRating(use_current_ratings=True)
            elo_rating.update_ratings(self.winner, self.loser)
            PlayerRating.add_ratings(elo_rating)

    class Meta:
        db_table = 'match'
        verbose_name = ('match')
        verbose_name_plural = ('matchs')


class PlayerRating(models.Model):
    """Table for keeping track of a player's rating."""
    player = models.OneToOneField(Player, default=None, primary_key=True, on_delete=models.CASCADE)
    rating = models.IntegerField(default=None, blank=False)
    
    @staticmethod
    def add_ratings(elo_rating: EloRating):
        """Add ratings to database given EloRating object."""
        PlayerRating.objects.all().delete()
        for player, rating in elo_rating.ratings.items():
            PlayerRating.objects.create(player=player, rating=rating)

    @staticmethod
    def generate_ratings():
        """Generate ratings from scratch based on all previous matches."""
        elo_rating = EloRating()
        matches = Match.objects.all().order_by('datetime')
        for match in matches:
            elo_rating.update_ratings(match.winner, match.loser)
        PlayerRating.add_ratings(elo_rating)

    @property
    def games_played(self):
        """Returns the number of games played."""
        games_played = self.wins + self.losses
        return games_played
        
    @property
    def losses(self):
        """Returns the number of losses."""
        losses = Match.objects.filter(loser=self.player).count()
        return losses

    @property
    def wins(self):
        """Returns the number of wins."""
        wins = Match.objects.filter(winner=self.player).count()
        return wins

    @property
    def points_won(self):
        """Returns the number of points won."""
        winning_matches = Match.objects.filter(winner=self.player)
        losing_matches = Match.objects.filter(loser=self.player)
        points_won = (
            winning_matches.aggregate(points=Coalesce(Sum('winning_score'), 0))['points']
            + losing_matches.aggregate(points=Coalesce(Sum('losing_score'), 0))['points']
        )
        return points_won

    @property
    def points_lost(self):
        """Returns the number of points lost."""
        winning_matches = Match.objects.filter(winner=self.player)
        losing_matches = Match.objects.filter(loser=self.player)
        points_lost = (
            winning_matches.aggregate(points=Coalesce(Sum('losing_score'), 0))['points']
            + losing_matches.aggregate(points=Coalesce(Sum('winning_score'), 0))['points']
        )
        return points_lost

    @property
    def points_per_game(self):
        """Returns the number of wins."""
        points_per_game = self.points_won / self.games_played
        return points_per_game

    @property
    def point_differential(self):
        """Return the points won minus points lost."""
        point_differential = self.points_won - self.points_lost
        return point_differential

    @property
    def avg_point_differential(self):
        """Return the avergae point differential."""
        avg_point_differential = self.point_differential / self.games_played
        return avg_point_differential

    @property
    def win_percent(self):
        """Return the win percentage."""
        win_percent = self.wins / self.games_played
        return win_percent

    @property
    def max_rating(self):
        max_rating = self.rating
        elo_rating = EloRating()
        matches = Match.objects.all().order_by('datetime')
        for match in matches:
            elo_rating.update_ratings(match.winner, match.loser)
            rating = elo_rating.get_rating(self.player)
            if (rating > max_rating):
                max_rating = rating

        return max_rating

    @property
    def rating_history_report(self):
        """Returns a history report of your rating."""
        rating_history = []

        elo_rating = EloRating()
        matches = Match.objects.all().order_by('datetime')
        for match in matches:
            elo_rating.update_ratings(match.winner, match.loser)
            rating_elem = {}
            rating_elem['x'] = match.datetime.timestamp()
            rating_elem['y'] = elo_rating.get_rating(self.player)
            rating_history.append(rating_elem)
        return rating_history

    @property
    def rating_history_days(self):
        """Returns a history report of your rating."""
        rating_history = []

        elo_rating = EloRating()
        matches = Match.objects.all().order_by('datetime')
        for match in matches:
            elo_rating.update_ratings(match.winner, match.loser)
            rating_history.append(RatingHistory(player=self.player, date=match.datetime.date(), rating=elo_rating.get_rating(self.player)))
        return rating_history

    class Meta:
        db_table = 'player_rating'
        verbose_name = ('player_rating')
        verbose_name_plural = ('player_ratings')


class Event(models.Model):
    name = models.CharField(verbose_name=('name'), max_length=255, null=False)

    class Meta:
        db_table = 'event'
        verbose_name = ('event')
        verbose_name_plural = ('events')


class RatingHistory(models.Model):
    player = models.ForeignKey(
        'Player',
        db_index=True,
        verbose_name=('player'),
        null=False,
        on_delete=models.CASCADE
    )
    date = models.DateField(db_index=True, verbose_name=('date'), null=False)
    rating = models.FloatField(null=False)

    def __str__(self):
        return "{0} {1}".format(self.player.full_name, self.date)