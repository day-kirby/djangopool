import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

class Team(models.Model):
    
    name = models.CharField(max_length=200)

    @property
    def win_count2(self):
        return self.winner.count()

    def __str__(self) -> str:
        return self.name

class Game(models.Model):
    team1 = models.ForeignKey(Team, related_name='team1', on_delete=models.DO_NOTHING)
    team2 = models.ForeignKey(Team, related_name='team2', on_delete=models.DO_NOTHING)
    winner = models.ForeignKey(Team, related_name='winner', on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return 'game on!'

