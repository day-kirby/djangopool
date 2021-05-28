from django.db import models

# note - none of these objects can be deleted through the app at this point

class Player(models.Model): # user of pool, not player on a team

    name = models.CharField(max_length=200, unique=True)

    @property
    def pick_count(self):
        return self.player.count()

    @property
    def win_count(self):
        # there should be a better way to do this!
        # e.g. get a set of all games where the winner is one of the picks
        # note that the "player" view has an alternative way to get list of wins
        # hoping to learn a one-liner for this
        picks = Pick.objects.filter(player=self.id)
        w = 0
        for p in picks:
            wins = Game.objects.filter(winner=p.team)
            w = w + wins.count()
        
        return w

    def __str__(self) -> str:
        return self.name

class Team(models.Model):
    
    name = models.CharField(max_length=200, unique=True)

    @property
    def win_count(self):
        # number of games that a team is the winner
        return self.winner.count()

    def __str__(self) -> str:
        return self.name

class Game(models.Model):
    # teams that played the game
    team1 = models.ForeignKey(Team, related_name='team1', on_delete=models.DO_NOTHING)
    team2 = models.ForeignKey(Team, related_name='team2', on_delete=models.DO_NOTHING)
    winner = models.ForeignKey(Team, related_name='winner', on_delete=models.DO_NOTHING)

    @property
    def differentTeams(self):
        return(self.team1 != self.team2)

    @property
    def validWinner(self):
        return((self.team1 == self.winner) or (self.team2 == self.winner))

    @property
    def statusMessage(self):
        msg = "OK"
        if(not self.validWinner):
            msg = 'winner must be one of the teams'
        if(not self.differentTeams):
            msg = 'teams must be different'
        #handled by form
        #if(not all_ids):
        #    msg = 'must choose two teams and a winner'
        return(msg)

    def __str__(self) -> str:
        return 'game on!'

class Pick(models.Model):

    # player by player id, team by team id - player x picks team y
    # nothing stops a player from having more than one identical pick
    # could be a quick validation step in the form
    # curious if this could be done with the model definition
    player = models.ForeignKey(Player, related_name='player', on_delete=models.DO_NOTHING)
    team = models.ForeignKey(Team, related_name='team', on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return 'good choice'

#models from original demo ---------

#class Question(models.Model):
#    question_text = models.CharField(max_length=200)
#    pub_date = models.DateTimeField('date published')
#    def __str__(self):
#        return self.question_text
#    def was_published_recently(self):
#        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

#class Choice(models.Model):
#    question = models.ForeignKey(Question, on_delete=models.CASCADE)
#    choice_text = models.CharField(max_length=200)
#    votes = models.IntegerField(default=0)
#    def __str__(self):
#        return self.choice_text
