from django.contrib import admin
from django.db import models
from django.forms import NumberInput

# Register your models here.
from .models import Teams, Players, Games, \
                    FielderResults, PitcherResults

admin.site.site_header = '栄冠ナインデータベース 管理画面'

class TeamsAdmin(admin.ModelAdmin):
    list_display = ('year', 'period', 'prefecture', \
                    'training_policy', 'draft_nomination', 'remark')

class PlayersAdmin(admin.ModelAdmin):
    list_display = ('name', 'admission_year', 'position' , 'is_ob', \
                    'is_active', 'is_genius', 'remark')

class FielderResultsInline(admin.TabularInline):
    model = FielderResults
    verbose_name = "野手"
    extra = 9
    formfield_overrides = {
        models.PositiveSmallIntegerField: \
            {'widget': NumberInput(attrs={'style':'width: 2em;'})}
    }

class PitcherResultsInline(admin.TabularInline):
    model = PitcherResults
    verbose_name = "投手"
    extra = 1
    formfield_overrides = {
        models.PositiveSmallIntegerField: \
            {'widget': NumberInput(attrs={'style':'width: 3em;'})}
    }

class GamesAdmin(admin.ModelAdmin):
    list_display = ('team_id', 'competition_type', 'competiton_round', \
                    'result', 'score', 'run', 'lank')
    inlines = [FielderResultsInline, PitcherResultsInline]

admin.site.register(Teams, TeamsAdmin)
admin.site.register(Players, PlayersAdmin)
admin.site.register(Games, GamesAdmin)