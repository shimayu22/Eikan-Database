from django.contrib import admin
from django.db import models
from django.forms import NumberInput

# Register your models here.
from .models import Teams, Players, Games, \
                    FielderResults, PitcherResults, \
                    PlayersFielder, PlayersPitcher

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

class PlayersFielderAdmin(admin.ModelAdmin):
    list_display = ('player_id',)

class PlayersPitcherAdmin(admin.ModelAdmin):
    list_display = ('player_id',)


admin.site.register(Teams, TeamsAdmin)
admin.site.register(Players, PlayersAdmin)
admin.site.register(Games, GamesAdmin)
admin.site.register(PlayersFielder, PlayersFielderAdmin)
admin.site.register(PlayersPitcher, PlayersPitcherAdmin)

from django.db.models.signals import post_save
from django.dispatch import receiver
from eikan import calculate_sabr as c

# 選手を登録したらPlayersFielder,PlayersPitcherも初期値でレコードを登録する

# チーム総合成績の更新
@receiver(post_save, sender=Games)
def update_cal_team_results(sender, instance, **kwargs):
    print("Admin")

# 野手成績の更新
@receiver(post_save, sender=FielderResults)
def update_cal_fielder_results(sender, instance, **kwargs):
    print(instance.player_id)
    c_s = c.CalculateFielderSabr(instance.player_id)
    print("更新しました")
    
# 投手成績の更新
@receiver(post_save, sender=PitcherResults)
def update_cal_pitcher_results(sender, instance, **kwargs):
    print(instance.innings_pitched)