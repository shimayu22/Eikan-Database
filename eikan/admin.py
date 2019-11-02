from django.contrib import admin

# Register your models here.
from .models import Teams, Players, Games, Fielder_results, Pitcher_results

class Fielder_resultsInline(admin.TabularInline):
    model = Fielder_results
    extra = 9

class Pitcher_resultsInline(admin.TabularInline):
    model = Pitcher_results
    extra = 1

class TeamsAdmin(admin.ModelAdmin):
    list_display = ('year', 'period', 'prefecture')

class PlayersAdmin(admin.ModelAdmin):
    list_display = ('admission_year', 'name' , 'position' , 'remark')

class GamesAdmin(admin.ModelAdmin):
    list_display = ('team_id', 'competition_type', 'competiton_round')
    inlines = [Pitcher_resultsInline]

admin.site.register(Teams, TeamsAdmin)
admin.site.register(Players, PlayersAdmin)
admin.site.register(Games, GamesAdmin)