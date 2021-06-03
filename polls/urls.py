from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='players'),
    path("players", views.index, name='players'),
    path("games", views.games, name='games'),   
    path("season", views.season, name='season'), # so that there can be a default mode
    path("season/<str:mode>", views.season, name='season'),  
    path("teams", views.teams, name='teams'),
    path("cbv", views.TeamsView.as_view()), # simple test for class-based view
    path("listview", views.TeamsListView.as_view()), # simple test for generic views
    path("player<int:id>", views.player, name='player'),
    path("editgame<int:id>", views.editgame, name='editgame'),
    path("deletepick<int:id>", views.deletepick, name='deletepick'),
]