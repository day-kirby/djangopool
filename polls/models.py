from django.db import models
from django.db.models import Avg, Count, Min, Sum

# note - none of these objects can be deleted through the app at this point

class PlayerManager(models.Manager):
    def with_picks(self):
        # the number of records (picks) where the player = self
        # seems that python is smart enough to know that Pick is the right model
        # without having to specify it, which is great (but not very explicit)
        pCount = Count("player") 

        # attempting to add win count as an annotation to player
        #a = Pick.objects.filter(player=self.id).values('team') 
        #t = Team.objects.filter(id__in=a).values("id")
        #w = Game.objects.filter(winner__in=t).count() 

        #wCount = Count("player__team__winner")

        return self.annotate(
            #win_count = wCount, #doesn't work
            pick_count = pCount
        )

class Player(models.Model): # user of pool, not player on a team

    name = models.CharField(max_length=200, unique=True)

    # get objects property with added feilds
    # note PlayerManager doesn't need argument, even though
    # it's expecting a manager object, 
    # python seems to pick this up in context
    objects = PlayerManager() 

    #this was moved to manager
    #@property
    #def pick_count(self):
    #    return self.player.count()

    def calculateNumTeams(self):
        nt = Pick.objects.filter(player=self.id).count()
        return nt

    teamCount = property(calculateNumTeams)

    @property
    def pickedTeams(self):
        return Pick.objects.filter(player=self.id)
     

    @property
    def win_count(self):

        # this works but i hate it
        #a = Pick.objects.filter(player=self.id).values('team') 
        #t = Team.objects.filter(id__in=a).values("id")
        #w = Game.objects.filter(winner__in=t).count() 

        # this is a bit better but would love a one-liner
        # or to put into manager
        player = Player.objects.get(id=self.id)
        #picks = Pick.objects.filter(player=self.id) - next line is equivalent
        picks = self.player.all()
        teams = Team.objects.filter(team__in=picks)
        wins = Game.objects.filter(winner__in=teams)
        #wins = self.player.all().winner.all() # this doesn't work
        w = wins.count()

        

        return w

    @property
    def win_count2(self):
        picks = Pick.objects.filter(player=self.id).select_related('team')

        # this works, but is inferior to win_count above
        w = 0
        for p in picks:
            wins = Game.objects.filter(winner=p.team)
            w = w + wins.count()
        
        return w

    def __str__(self) -> str:
        return self.name

class TeamManager(models.Manager):
    def with_wins(self):
        return self.annotate(
            win_count = Count('winner')
        )

class Team(models.Model):
    
    name = models.CharField(max_length=200, unique=True)
    imageFileName = models.CharField(max_length=200, default="file.jpg")
    objects = TeamManager()

    #moved this to a manager
    #@property
    #def win_count(self):
    #    # number of games that a team is the winner
    #    return self.winner.count()
    
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



#class Season():


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
