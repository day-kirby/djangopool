from django import forms
from django.db.models import fields
from .models import Team, Game, Player, Pick

class NavigatePlayersForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ["player"]

    player = forms.ModelChoiceField(queryset=Player.objects.all().order_by('name'))

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

    # filter the teams list to not include already picked teams
    # this works, and it's suprising that
    # i didn't need to reference ModelChoiceField to make this work
    def __init__(self, playerId, *args, **kwargs): # needed this to pass the player id in
        super(CreateNewPick, self).__init__(*args, **kwargs) 
        pickedTeams = Pick.objects.filter(player=playerId).values('team_id')
        availTeams = Team.objects.exclude(id__in=pickedTeams).order_by('name')
        self.fields['team'].queryset = availTeams # this sets the choices for the dropdown

class CreateNewGame(forms.ModelForm):
    class Meta: 
        model = Game
        fields = ["team1", "team2", "winner"]

    team1 = forms.ModelChoiceField(queryset=Team.objects.all().order_by('name'))
    team2 = forms.ModelChoiceField(queryset=Team.objects.all().order_by('name'))
    winner = forms.ModelChoiceField(queryset=Team.objects.all().order_by('name'))