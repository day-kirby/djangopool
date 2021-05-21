
from django.http import response
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Count
from .models import Game, Team, Player, Pick
from .forms import CreateNewPlayer, CreateNewTeam, CreateNewGame, CreateNewPick

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

    player = Player.objects.get(id=id)
    picks = Pick.objects.filter(player=player.id)

    # don't really need these, they are just for testing / experimenting
    pick_ids = Pick.objects.filter(player=player.id).values('team_id') # returns id's of picked teams
    picked_teams = Team.objects.filter(id__in=pick_ids)  # return queryset from Team filtered on the picks
    winning_games = Game.objects.filter(winner__in=picked_teams) # returns queryset from Game where winners are only picked teams

    if (request.method == 'POST'):
        form = CreateNewPick(request.POST)
        if(form.is_valid()):    
            team = form.cleaned_data["team"]
            pk = Pick(player=player,team=team)
            pk.save()
    else:
        form = CreateNewPick()

   
    context = { # too much sent to template, just for testing
        'p': player, 
        'picks': picks, 
        'form': form, 
        'picked_teams': picked_teams, 
        'winning_games': winning_games 
    }
    return render(request, 'polls/player.html', context)

def editgame(request, id):
    gm = Game.objects.get(id=id)

    # for testing, these are not needed
    #tm1 = Team.objects.get(id=gm.team1_id)
    #tm2 = Team.objects.get(id=gm.team2_id)
    #winner = Team.objects.get(id=gm.winner_id)

    if request.method == 'POST':
        form = CreateNewGame(request.POST, instance=gm)
        if(form.is_valid()):    
            form.save()     
        context = { 'game': gm, 'form': form }  

        #testing version:
        #context = { 'game': gm, 'team1_name': tm1.name, 'team2_name': tm2.name, 'winner_name': winner.name, 'form': form } 
        return render(request, 'polls/game.html', context)
    else:

        form = CreateNewGame(instance=gm)

        context = { 'game': gm, 'form': form }  

        #testing version:
        #context = { 'game': gm, 'team1_name': tm1.name, 'team2_name': tm2.name, 'winner_name': winner.name, 'form': form }
        return render(request, 'polls/game.html', context)

def games(request):
    gms = Game.objects.all()

    if request.method == 'POST':
        form = CreateNewGame(request.POST)
        if(form.is_valid()):
            
            t1 = form.cleaned_data["team1"]
            t2 = form.cleaned_data["team2"]
            w = form.cleaned_data["winner"]

            g = Game(team1=t1, team2=t2, winner=w)

            t1_id = g.team1_id
            t2_id = g.team2_id
            w_id = g.winner_id

            # there is a team1, team2 and winner
            all_ids= (t1_id > 0) and (t1_id > 0) and (w_id > 0)
            # team 1 and 2 are different
            diff_teams = (t1_id != t2_id)
            # winner is one of the teams
            valid_winner = (t1_id == w_id) or (t2_id == w_id)

            if(all_ids and diff_teams and valid_winner):
                
                g.save()

                form = CreateNewGame()
                context = { 'games': gms, 'form': form, 'msg': '' }
                return render(request, 'polls/games.html', context)

            else: 
                # msg appears in template
                # probably better that this content is in template
                # and that their visibility is controlled by a status variable
                # eg status = 'same_teams'
                msg = 'invalid!'
                if(not valid_winner):
                    msg = 'winner must be one of the teams'
                if(not diff_teams):
                    msg = 'teams must be different'
                if(not all_ids):
                    msg = 'must choose two teams and a winner'
                context = { 'games': gms, 'form': form, 'msg': msg }
                return render(request, 'polls/games.html', context)

    else:
        form = CreateNewGame()

        context = { 'games': gms, 'form': form, 'msg': '' }
        return render(request, 'polls/games.html', context)

def teams(request):
    tms = Team.objects.all()

    if request.method == 'POST':
        form = CreateNewTeam(request.POST)
        if(form.is_valid()):
            n = form.cleaned_data["name"]
            t = Team(name=n)
            t.save()

    else:
        form = CreateNewTeam()

    gms = Game.objects.all()

    context = { 'teams': tms, 'form': form }
    return render(request, 'polls/teams.html', context)

