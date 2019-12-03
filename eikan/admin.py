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
    list_display = ('player_id', 'ops', 'slg', 'obp', 'gpa', 'batting_average', 'at_bat', \
                    'run', 'hit', 'two_base', 'three_base', 'home_run', 'run_batted_in', \
                    'strike_out', 'bb_hbp', 'sacrifice_bunt', 'stolen_base', 'grounded_into_double_play', \
                    'error', 'total_bases', 'bbhp_percent', 'isod', 'isop', 'bbhp_k', 'p_s',)

class PlayersPitcherAdmin(admin.ModelAdmin):
    list_display = ('player_id', 'era', 'whip', 'k_bbhp', 'k_9', 'k_percent', 'bbhp_9', \
                    'p_bbhp_percent', 'hr_9', 'hr_percent', 'lob_percent', 'p_ip', 'ura', \
                    'games_started', 'innings_pitched', 'total_batters_faced', 'number_of_pitch', \
                    'hit', 'strike_out', 'bb_hbp', 'run', 'earned_run', 'wild_pitch', 'home_run',)


admin.site.register(Teams, TeamsAdmin)
admin.site.register(Players, PlayersAdmin)
admin.site.register(Games, GamesAdmin)
admin.site.register(PlayersFielder, PlayersFielderAdmin)
admin.site.register(PlayersPitcher, PlayersPitcherAdmin)

from django.db.models.signals import post_save
from django.dispatch import receiver
from eikan import calculate_sabr as c

# 選手を登録したらPlayersFielder,PlayersPitcherも対応するレコードを登録する
@receiver(post_save, sender=Players)
def insert_new_player_results(sender, instance, **kwargs):
    PlayersFielder.objects.create(player_id=instance)
    if instance.is_pitcher:
        PlayersPitcher.objects.create(player_id=instance)

# チーム総合成績の更新
@receiver(post_save, sender=Games)
def update_cal_team_results(sender, instance, **kwargs):
    print("Admin")

# 野手成績の更新
@receiver(post_save, sender=FielderResults)
def update_cal_fielder_results(sender, instance, **kwargs):
    print(instance.player_id)
    cs = c.CalculateFielderSabr(instance.player_id)
    cs.update_total_results()
    
# 投手成績の更新
@receiver(post_save, sender=PitcherResults)
def update_cal_pitcher_results(sender, instance, **kwargs):
    print(instance.innings_pitched)