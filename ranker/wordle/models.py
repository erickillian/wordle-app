from django.db import models
from django.utils.translation import gettext_lazy as _
from ranker.users.models import Player

from ranker.wordle.constants.wordle import WORDLE_MAX_LENGTH, WORDLE_NUM_GUESSES

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
                    word_copy.pop(word_copy.index(letter))

            for j, letter in enumerate(guess):
                if letter == self.word[j]:
                    correct += "2"
                    if letter in word_copy:
                        word_copy.pop(word_copy.index(letter))
                elif letter in word_copy:
                    correct += "1"
                    word_copy.pop(word_copy.index(letter))
                else:
                    correct += "0"
        return correct

    @property
    def guesses(self):
        return int(len(self.guess_history) / WORDLE_MAX_LENGTH)

    class Meta:
        db_table = 'active_wordle'
        verbose_name = ('Active Wordle')
        verbose_name_plural = ('Active Wordles')
            

class Wordle(models.Model):
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
