from django import forms
from django.db.models import fields
from .models import Team, Game

class CreateNewTeam(forms.Form):
    name = forms.CharField(label="Team name", max_length=200)

class CreateNewGame(forms.ModelForm):
    class Meta: 
        model = Game
        fields = ["team1", "team2", "winner"]

    team1 = forms.ModelChoiceField(queryset=Team.objects.all().order_by('name'))
    team2 = forms.ModelChoiceField(queryset=Team.objects.all().order_by('name'))
    winner = forms.ModelChoiceField(queryset=Team.objects.all().order_by('name'))
