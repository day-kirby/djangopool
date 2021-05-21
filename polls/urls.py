from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='players'),
    path("players", views.index, name='players'),
    path("games", views.games, name='games'),
    path("teams", views.teams, name='teams'),
    path("player<int:id>", views.player, name='player'),
    path("editgame<int:id>", views.editgame, name='editgame'),
]