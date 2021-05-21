from django import forms
from django.db.models import fields
from .models import Team, Game, Player, Pick

class CreateNewPlayer(forms.ModelForm):
    class Meta: 
        model = Player
        fields = ["name"]

    name = forms.CharField(label="Player name", max_length=200)

class CreateNewTeam(forms.Form):
    name = forms.CharField(label="Team name", max_length=200)

class CreateNewPick(forms.ModelForm):
    class Meta: 
        model = Pick
        fields = ["team"] # player not needed, will be selected in the forms's context
        #fields = ["player", "team"]

    #player = forms.ModelChoiceField(queryset=Player.objects.all().order_by('name'))
    team = forms.ModelChoiceField(queryset=Team.objects.all().order_by('name'))

class CreateNewGame(forms.ModelForm):
    class Meta: 
        model = Game
        fields = ["team1", "team2", "winner"]

    team1 = forms.ModelChoiceField(queryset=Team.objects.all().order_by('name'))
    team2 = forms.ModelChoiceField(queryset=Team.objects.all().order_by('name'))
    winner = forms.ModelChoiceField(queryset=Team.objects.all().order_by('name'))