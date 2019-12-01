from django.db import models
from eikan.models import Games, Players, Teams

def set_select_players():
    teams = Teams.objects.latest('pk')
    count = Teams.objects.count()
    condition_dict = {}
    
    if count > 0:
        condition_dict["admission_year__gte"] = \
            (teams.year - 2) if teams.period == 1 \
                             else (teams.year - 1)
        
        condition_dict["admission_year__lte"] = teams.year
    
    return condition_dict

# Create your models here.
class FielderResults(models.Model):

    game_id = models.ForeignKey(
        Games,
        on_delete=models.CASCADE,
    )

    player_id = models.ForeignKey(
        Players,
        on_delete=models.CASCADE,
        verbose_name="選手",
        limit_choices_to=set_select_players,
    )

    at_bat = models.PositiveSmallIntegerField(
        verbose_name="打数",
        default=0,
    )

    run = models.PositiveSmallIntegerField(
        verbose_name="得点",
        default=0,
    )

    hit = models.PositiveSmallIntegerField(
        verbose_name="安打",
        default=0,
    )

    two_base = models.PositiveSmallIntegerField(
        verbose_name="二塁打",
        default=0,
    )

    three_base = models.PositiveSmallIntegerField(
        verbose_name="三塁打",
        default=0,
    )

    home_run = models.PositiveSmallIntegerField(
        verbose_name="本塁打",
        default=0,
    )

    run_batted_in = models.PositiveSmallIntegerField(
        verbose_name="打点",
        default=0,
    )

    strike_out = models.PositiveSmallIntegerField(
        verbose_name="三振",
        default=0,
    )

    bb_hbp = models.PositiveSmallIntegerField(
        verbose_name="四死球",
        default=0,
    )

    sacrifice_bunt = models.PositiveSmallIntegerField(
        verbose_name="犠打",
        default=0,
    )

    stolen_base = models.PositiveSmallIntegerField(
        verbose_name="盗塁",
        default=0,
    )

    grounded_into_double_play = models.PositiveSmallIntegerField(
        verbose_name="併殺",
        default=0,
    )

    error = models.PositiveSmallIntegerField(
        verbose_name="失策",
        default=0,
    )

    created_at = models.DateTimeField(
        verbose_name="登録日",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        verbose_name="更新日",
        auto_now=True,
    )

    def __str__(self):
        return f'{self.game_id}:{self.player_id}'

    class Meta:
        verbose_name = "打者一覧"
        verbose_name_plural = "打者成績"
