from django.contrib import admin
from django.db import models
from django.forms import NumberInput

# Register your models here.
from .models import Teams, Players, Games, \
                    FielderResults, PitcherResults, \
                    FielderTotalResults, PitcherTotalResults, \
                    TeamsTotalResults

admin.site.site_header = '栄冠ナインデータベース 管理画面'

class TeamsAdmin(admin.ModelAdmin):
    fields = (('year', 'period', 'prefecture'), 'training_policy', \
              'draft_nomination', 'remark')
    list_display = ('year', 'period', 'prefecture', 'training_policy', \
                    'draft_nomination', 'remark')

class PlayersAdmin(admin.ModelAdmin):
    fields = ('name', 'admission_year', 'position', ('is_pitched' , \
              'is_ob', 'is_active', 'is_genius'), 'remark')
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
    fields = ('team_id', ('competition_type', 'competiton_round'), \
                    ('result', 'score', 'run'), 'rank')
    list_display = ('team_id', 'competition_type', 'competiton_round', \
                    'result', 'score', 'run', 'rank')
    inlines = [FielderResultsInline, PitcherResultsInline]

class TeamTotalResultsAdmin(admin.ModelAdmin):
    list_display = ('team_id', 'rank', 'total_win', 'total_lose', 'total_draw', 'score', \
                    'run', 'score_difference', 'batting_average', 'ops', 'hr', 'era', 'der', 'remark')

class FielderTotalResultsAdmin(admin.ModelAdmin):
    list_display = ('player_id', 'ops', 'slg', 'obp', 'gpa', 'batting_average', 'at_bat', \
                    'run', 'hit', 'two_base', 'three_base', 'home_run', 'run_batted_in', \
                    'strike_out', 'bb_hbp', 'sacrifice_bunt', 'stolen_base', 'grounded_into_double_play', \
                    'error', 'total_bases', 'bbhp_percent', 'isod', 'isop', 'bbhp_k', 'p_s',)

class PitcherTotalResultsAdmin(admin.ModelAdmin):
    list_display = ('player_id', 'era', 'whip', 'k_bbhp', 'k_9', 'k_percent', 'bbhp_9', \
                    'p_bbhp_percent', 'hr_9', 'hr_percent', 'lob_percent', 'p_ip', 'ura', \
                    'games', 'games_started', 'innings_pitched', 'total_batters_faced', 'number_of_pitch', \
                    'hit', 'strike_out', 'bb_hbp', 'run', 'earned_run', 'wild_pitch', 'home_run',)


admin.site.register(Teams, TeamsAdmin)
admin.site.register(Players, PlayersAdmin)
admin.site.register(Games, GamesAdmin)
admin.site.register(FielderTotalResults, FielderTotalResultsAdmin)
admin.site.register(PitcherTotalResults, PitcherTotalResultsAdmin)
admin.site.register(TeamsTotalResults, TeamTotalResultsAdmin)

from django.db.models.signals import post_save
from django.dispatch import receiver
from eikan import calculate_sabr as c

# チームを登録したらTeamsTotalResultsも対応するレコードを登録する
@receiver(post_save, sender=Teams)
def insert_new_teams_total_results(sender, instance, **kwargs):
    TeamsTotalResults.objects.create(team_id=instance, year=instance.year, \
                                     period=instance.period, remark=instance.remark)

# 選手を登録したらFielderTotalResults,
# PitcherTotalResultsも対応するレコードを登録する
@receiver(post_save, sender=Players)
def insert_new_player_results(sender, instance, **kwargs):
    FielderTotalResults.objects.get_or_create(player_id=instance)
    if instance.is_pitcher:
        PitcherTotalResults.objects.get_or_create(player_id=instance)

# 更新順序の関係で行う（できればもっとスマートな方法でやりたい）
@receiver(post_save, sender=Games)
def update_teams_total_results_updated_at(sender,instance, **kwargs):
    TeamsTotalResults.objects.get(team_id=instance.team_id).save()

# 野手成績の更新
@receiver(post_save, sender=FielderResults)
def update_cal_fielder_results(sender, instance, **kwargs):
    cs = c.CalculateFielderSabr(instance.player_id)
    cs.update_total_results()
    
# 投手成績の更新
@receiver(post_save, sender=PitcherResults)
def update_cal_pitcher_results(sender, instance, **kwargs):
    cs = c.CalculatePitcherSabr(instance.player_id)
    cs.update_total_results()

# チーム総合成績の更新
@receiver(post_save, sender=PitcherTotalResults)
def update_cal_team_results(sender, instance, **kwargs):
    # 投手の新規登録時に実行しないようにする
    # できればこの方法やめたい
    if instance.created_at == instance.updated_at:
        pass
    else:
        team_id = TeamsTotalResults.objects.latest('updated_at').team_id
        cs = c.CalculateTeamSabr(team_id)
        cs.update_total_results()