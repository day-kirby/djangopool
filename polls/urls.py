from django.urls import path, include

from . import views

urlpatterns = [
    path('test', views.test, name='test'),
    path('', views.index, name='index'),
    path("<int:id>", views.index, name='index'),
    path("editgame<int:id>", views.editgame, name='editgame'),
    path("editgame", views.editgame, name='editgame'),
    path("games", views.games, name='games'),
    path("teams", views.teams, name='teams'),
]