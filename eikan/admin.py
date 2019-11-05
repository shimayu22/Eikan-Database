from django.contrib import admin
from django.db import models
from django.forms import NumberInput

# Register your models here.
from .models import Teams, Players, Games, Fielder_results, Pitcher_results

class Fielder_resultsInline(admin.TabularInline):
    model = Fielder_results
    verbose_name = "野手"
    extra = 9
    formfield_overrides = {
        models.PositiveSmallIntegerField: {'widget': NumberInput(attrs={'style':'width: 2.5em;'})}
    }

class Pitcher_resultsInline(admin.TabularInline):
    model = Pitcher_results
    verbose_name = "投手"
    extra = 1
    formfield_overrides = {
        models.PositiveSmallIntegerField: {'widget': NumberInput(attrs={'style':'width: 2.5em;'})}
    }

class TeamsAdmin(admin.ModelAdmin):
    list_display = ('year', 'period', 'prefecture', 'training_policy', 'draft_nomination', 'remark')

class PlayersAdmin(admin.ModelAdmin):
    list_display = ('admission_year', 'name' , 'position' , 'remark')

class GamesAdmin(admin.ModelAdmin):
    list_display = ('team_id', 'competition_type', 'competiton_round', 'result', 'score', 'run', 'lank')
    inlines = [Fielder_resultsInline, Pitcher_resultsInline]

admin.site.register(Teams, TeamsAdmin)
admin.site.register(Players, PlayersAdmin)
admin.site.register(Games, GamesAdmin)