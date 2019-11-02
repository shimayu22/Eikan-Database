from django.contrib import admin

# Register your models here.
from .models import Teams, Players, Games, Fielder_results, Pitcher_results

class TeamsAdmin(admin.ModelAdmin):
    list_display = ('year', 'period', 'prefecture')

class PlayersAdmin(admin.ModelAdmin):
    list_display = ('admission_year', 'name' , 'position' , 'remark')

class GamesAdmin(admin.ModelAdmin):
    list_display = ('team_id', 'competition_type', 'competiton_round')

class Fielder_resultsAdmin(admin.ModelAdmin):
    list_display = ('player_id', 'game_id')

class Pitcher_resultsAdmin(admin.ModelAdmin):
    list_display = ('player_id', 'game_id')
    

admin.site.register(Teams, TeamsAdmin)
admin.site.register(Players, PlayersAdmin)
admin.site.register(Games, GamesAdmin)
admin.site.register(Fielder_results, Fielder_resultsAdmin)
admin.site.register(Pitcher_results, Pitcher_resultsAdmin)