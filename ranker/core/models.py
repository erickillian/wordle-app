from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from ranker.core.rankings import EloRating
import json
import os
import random



from ranker.core.constants.wordle import WORDLE_MAX_LENGTH, WORDLE_NUM_GUESSES
from ranker.settings.dev import BASE_DIR


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, username, firstname, lastname, password, **other_fields):
        """
        Creates and saves a superuser with the given info.
        """

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') != True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.'
            )
        if other_fields.get('is_superuser') != True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.'
            )

        return self.create_user(email, username, firstname, lastname, password, **other_fields)

    def create_user(self, email, username, firstname, lastname, password, **other_fields):
        """
        Creates and saves a user with the given info.
        """
        if not email:
            raise ValueError(_('You must provide an email address'))

        if not username:
            raise ValueError(_('You must provide an user name'))

        email = BaseUserManager.normalize_email(email)
        user = Player(email=email, username=username,
                          firstname=firstname, lastname=lastname, **other_fields)

        user.set_password(password)
        user.save()
        return user

class Player(AbstractBaseUser, PermissionsMixin):
    """Table for keeping player information."""
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=150, unique=True)
    firstname = models.CharField(max_length=150, blank=True)
    lastname = models.CharField(max_length=150, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'firstname', 'lastname']

    def __str__(self):
        """Display player's full name as string object representation."""
        return self.full_name

    @property
    def full_name(self):
        """The players full name, first plus last name."""
        full_name = f'{self.firstname} {self.lastname}'
        return full_name

    class Meta:
        db_table = 'player'
        verbose_name = ('player')
        verbose_name_plural = ('players')

class ActiveWordle(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    guess_history = models.CharField(max_length=WORDLE_MAX_LENGTH*WORDLE_NUM_GUESSES, blank=True)
    word = models.CharField(max_length=WORDLE_MAX_LENGTH, blank=False)

    @property
    def solved(self):
        return self.guess_history[-WORDLE_MAX_LENGTH:] == self.word

    @property
    def date(self):
        return self.start_time.date()

    @property
    def correct(self):
        correct = ""
        for i in range(0, int(len(self.guess_history) / WORDLE_MAX_LENGTH)):
            guess = self.guess_history[i*WORDLE_MAX_LENGTH:(i+1)*WORDLE_MAX_LENGTH]
            word_copy = list(self.word)
            for j, letter in enumerate(guess):
                if letter == self.word[j]:
                    correct += "2"
                    word_copy.pop(word_copy.index(letter))
                elif letter in word_copy:
                    correct += "1"
                    word_copy.pop(word_copy.index(letter))
                else:
                    correct += "0"
                j += 1
        return correct

    @property
    def guesses(self):
        return int(len(self.guess_history) / WORDLE_MAX_LENGTH)

    class Meta:
        db_table = 'active_wordle'
        verbose_name = ('active_wordle')
        verbose_name_plural = ('active_wordles')
            

class DailyWordle(models.Model):
    player = models.ForeignKey(Player, default=None,on_delete=models.CASCADE)
    word = models.CharField(max_length=5, blank=False)
    guesses = models.PositiveSmallIntegerField(blank=False)
    date = models.DateField(auto_now_add=True, blank=False)
    time = models.DurationField()
    fail = models.BooleanField(blank=False)
    class Meta:
        db_table = 'wordle'
        verbose_name = ('wordle')
        verbose_name_plural = ('wordles')


class Match(models.Model):
    """Table for keeping track of game scores and winners."""
    winner = models.ForeignKey(Player, default=None, related_name='won_matches',on_delete=models.CASCADE)
    winning_score = models.IntegerField(default=None)
    loser = models.ForeignKey(Player, default=None, related_name='lost_matches', on_delete=models.CASCADE)
    losing_score = models.IntegerField(default=None)
    datetime = models.DateTimeField(auto_now_add=True)

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


class Game(models.Model):
    name = models.CharField(max_length=60, blank=False)
    # Points it takes to win the game
    winning_points = models.PositiveIntegerField(blank=False, default=11)
    # Points ahead you have to be to win
    winning_point_differential = models.PositiveIntegerField(blank=False, default=0)

class PlayerRating(models.Model):
    """Table for keeping track of a player's rating."""
    player = models.OneToOneField(Player, default=None, primary_key=True, on_delete=models.CASCADE)
    rating = models.IntegerField(default=None, blank=False)
    # game = models.ManyToOneField(Player, blank=False, default=None, primary_key=True, on_delete=models.CASCADE)
    
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
        date = timezone.now()

        elo_rating = EloRating()
        matches = Match.objects.all().order_by('datetime')
        for match in matches:
            elo_rating.update_ratings(match.winner, match.loser)
            rating = elo_rating.get_rating(self.player)
            if (rating > max_rating):
                max_rating = rating
                date = match.date

        return {'rating': max_rating, 'date': date}

    @property
    def rating_trend(self):
        rating_history_days = self.rating_history_days
        values = [o.rating for o in rating_history_days[-5:]]
        return values

    @property
    def rating_history_days(self):
        """Returns a history report of your rating."""
        rating_history = []

        elo_rating = EloRating()
        matches = Match.objects.all().order_by('datetime')
        for match in matches:
            elo_rating.update_ratings(match.winner, match.loser)
            for rh_elem in rating_history: # Removes Rating history elements on the same day
                if rh_elem.date == match.datetime.date():
                    rating_history.remove(rh_elem)

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

# Only used to generate rating history reports, not populated in database
class RatingHistory(models.Model):
    player = models.ForeignKey(
        'Player',
        db_index=True,
        verbose_name=('player'),
        null=False,
        on_delete=models.CASCADE
    )
    date = models.DateField(db_index=True, verbose_name=('date'), null=False)
    rating = models.IntegerField(null=False)

    def __str__(self):
        return "{0} {1} {2}".format(self.player.full_name, self.date, self.rating)