from django import template

register = template.Library()

@register.simple_tag
def season_header():
    return "Season Stats"

@register.inclusion_tag("polls/season_grid.html")
def season_grid(teams, gms, mode):
    if(mode==None):
        mode = "games"

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
    return {
        'grid':gameGrid 
    }
