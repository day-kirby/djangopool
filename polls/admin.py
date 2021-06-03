from django.contrib import admin


from .models import Team, Game, Pick, Player

myModels = [Team, Game, Pick, Player]
admin.site.register(myModels)