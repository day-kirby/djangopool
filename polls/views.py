
from django.http import response, HttpResponse
from django.http.response import HttpResponseRedirect
from django.views import View
from django.views.generic import ListView
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Count
from django.conf.urls.static import static
from .models import Game, Team, Player, Pick
from .forms import CreateNewPlayer, CreateNewTeam, CreateNewGame, CreateNewPick, NavigatePlayersForm


def index(request): # root of app lists players, could have called this view "players"
    players = Player.objects.all()

    if request.method == 'POST':
        form = CreateNewPlayer(request.POST)
        if(form.is_valid()):
            n = form.cleaned_data["name"]
            p = Player(name=n)
            p.save()

    else:
        form = CreateNewPlayer()

    context = { 'players': players, 'form': form }
    return render(request, 'polls/players.html', context)


def player(request, id):

    players = Player.objects.with_picks() # includes annotation pick_count
    player = players.get(id=id)
    picks = player.pickedTeams # equiv to Pick.objects.filter(player=player)
    


    # don't really need these, they are just for testing / experimenting
    # note that gettting the queryset with just the id's was not necessary
    #pick_ids = Pick.objects.filter(player=player.id).values('team_id') # returns id's of picked teams
    #picked_teams = Team.objects.filter(id__in=pick_ids)  # return queryset from Team filtered on the picks
    #picked_wins = Game.objects.filter(winner__in=picked_teams) # returns queryset from Game where winners are only picked teams

    # the next two lines do the same job as the 3 lines above
    pt = Team.objects.filter(team__in=picks)
    pw = Game.objects.filter(winner__in=pt)

    # this line combines the previous two, and works
    # is there any performance savings to do it this way?
    #pw_oneline = Game.objects.filter(winner__in=Team.objects.filter(team__in=picks))

    if (request.method == 'POST'):
        if ('select_player' in request.POST):
            # navigation

            navForm = NavigatePlayersForm(request.POST)
            print(navForm) # for some reason removing this breaks it :(
            dropdownPlayer = navForm.cleaned_data["player"]

            playerUrl = "player" + str(dropdownPlayer.id)
            return (HttpResponseRedirect(playerUrl))

        else:
            # creating a new pick
            form = CreateNewPick(id, request.POST)
            if(form.is_valid()):    
                team = form.cleaned_data["team"]
                pk = Pick(player=player,team=team)
                pk.save()
    else:
        form = CreateNewPick(id)

    navForm = NavigatePlayersForm()

    context = { 
        'p': player, 
        'players': players, #for navigation
        'picks': picks,
        'picked_wins': pw,
        'navForm': navForm,
        'form': form, 
    }
    return render(request, 'polls/player.html', context)

def editgame(request, id):
    gm = Game.objects.get(id=id)

    if request.method == 'POST':
        form = CreateNewGame(request.POST, instance=gm)
        msg = ""
        if(form.is_valid()):    

            # create in-memory game in order to validate it
            tempGame = form.save(commit=False)
            msg = tempGame.statusMessage

            if(msg == "OK"):
                form.save()     

        context = { 'game': gm, 'form': form, 'msg': msg }  

        return render(request, 'polls/game.html', context)
    else:

        form = CreateNewGame(instance=gm)

        context = { 'game': gm, 'form': form }  

        #testing version:
        #context = { 'game': gm, 'team1_name': tm1.name, 'team2_name': tm2.name, 'winner_name': winner.name, 'form': form }
        return render(request, 'polls/game.html', context)

def season(request, mode=None):
    gms = Game.objects.all()
    teams = Team.objects.with_wins()

    if(mode==None):
        mode = "games"

    # all of the grid stuff below has been moved into a template tag
    # which is much nicer. however at the moment i still need this
    # in this view function for the javaScript version, which 
    # i can fix later

    gameGrid = []
    for t1 in teams:
        gameGridRow = []
        for t2 in teams:

            # default values
            # won't be replaced when teams are compared with themselves
            gameCount = "-"
            homeGames = "-"
            awayGames = "-"
            homeWins = "-"
            winCount = "-"

            value = "-"

            if(t1 != t2): # games are never between a team and itself
                hg = gms.filter(team1=t1,team2=t2)
                homeGames = hg.count()
                ag = gms.filter(team2=t1,team1=t2)
                awayGames = ag.count()
                gameCount = homeGames + awayGames

                #wins = t1.win_count # this is wrong - this counts across teams

                winningHomeGames = hg.filter(winner=t1)
                winningAwayGames = ag.filter(winner=t1)
                winCount = winningHomeGames.count() + winningAwayGames.count()

                # note py 3.10 includes a "match" method for this kind of thing
                if(mode == 'games'):
                    value = gameCount
                elif(mode == 'wins'):
                    value = winCount
                elif(mode == 'home'):
                    value = homeGames
            
            gameProps = {
                # for js version, need all values in the dom
                'games': gameCount, 
                'away': awayGames,
                'home': homeGames,
                'wins': winCount,
                # only need value for 'django' version
                'value': value
            }

            gameGridRow.append(gameProps)
        gameGrid.append({ 'name': t1.name, 'row': gameGridRow })

    gridMode = 'homeGames'

    context = { 'games': gms, 'teams': teams, 'grid': gameGrid, 'gridMode': mode, 'msg': '' }

    return render(request, 'polls/season.html', context)

def games(request):
    gms = Game.objects.all()
    teams = Team.objects.all()

    context = { 'games': gms, 'teams': teams, 'msg': '' }

    if request.method == 'POST':
        form = CreateNewGame(request.POST)
        if(form.is_valid()):
            
            t1 = form.cleaned_data["team1"]
            t2 = form.cleaned_data["team2"]
            w = form.cleaned_data["winner"]

            g = Game(team1=t1, team2=t2, winner=w)

            msg = g.statusMessage

            if(msg == "OK"):  
                g.save()

                form = CreateNewGame()
                context['form'] = form
                return render(request, 'polls/games.html', context)

            else: 
                # msg appears in template
                # probably better that this content is in template
                # and that their visibility is controlled by a status variable
                # eg status = 'same_teams'

                context['form'] = form
                return render(request, 'polls/games.html', context)

    else:
        form = CreateNewGame()

        context['form'] = form
        return render(request, 'polls/games.html', context)

class TeamsListView(ListView):
    model = Team
    template_name = "polls/teams_listview.html"

class TeamsView(View):

    test = "test"  
    tms = Team.objects.with_wins() 

    def get(self, request):
        #
        return HttpResponse(self.test)

class TeamsViewSub(TeamsView): # tiny cbv inheritance test
    test = "woah"

def teams(request):
    tms = Team.objects.with_wins().order_by('id')

    if request.method == 'POST':
        form = CreateNewTeam(request.POST)
        if(form.is_valid()):
            n = form.cleaned_data["name"]
            t = Team(name=n)
            t.save()

    else:
        form = CreateNewTeam()

    context = { 'teams': tms, 'form': form }
    return render(request, 'polls/teams.html', context)

def showpick(request, id):

    pick = Pick.objects.get(id=id)
    player = pick.player
    player_id = player.id

    playerUrl = "player" + str(player_id)

    context = { 'pick': pick, 'player': player, 'id': player_id, 'url': playerUrl }
    return render(request, 'polls/pick.html', context)

def deletepick(request, id):

    pick = Pick.objects.get(id=id)
    player = pick.player
    player_id = player.id

    playerUrl = "player" + str(player_id)

    pick.delete()

    return (HttpResponseRedirect(playerUrl))

