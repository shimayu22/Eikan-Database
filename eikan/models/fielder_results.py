from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator

from eikan.models import Games,Players

# Create your models here.
class Fielder_results(models.Model):
    game_id = models.ForeignKey(
        Games,
        on_delete=models.CASCADE,
    )

    player_id = models.ForeignKey(
        Players,
        on_delete=models.CASCADE,
        verbose_name = "選手",
        # TODO: 試合がある年度に在籍している選手だけ表示したい
    )

    at_bat = models.PositiveSmallIntegerField(
        verbose_name = "打数",
        default = 0,
    )

    run = models.PositiveSmallIntegerField(
        verbose_name = "得点",
        default = 0,
    )

    hit = models.PositiveSmallIntegerField(
        verbose_name = "安打",
        default = 0,
    )

    two_base = models.PositiveSmallIntegerField(
        verbose_name = "二塁打",
        default = 0,
    )

    three_base = models.PositiveSmallIntegerField(
        verbose_name = "三塁打",
        default = 0,
    )

    home_run = models.PositiveSmallIntegerField(
        verbose_name = "本塁打",
        default = 0,
    )

    run_batted_in = models.PositiveSmallIntegerField(
        verbose_name = "打点",
        default = 0,
    )

    strike_out = models.PositiveSmallIntegerField(
        verbose_name = "三振",
        default = 0,
    )

    bases_on_balls = models.PositiveSmallIntegerField(
        verbose_name = "四球",
        default = 0,
    )

    hit_by_pitch = models.PositiveSmallIntegerField(
        verbose_name = "死球",
        default = 0,
    )

    sacrifice_bunt = models.PositiveSmallIntegerField(
        verbose_name = "犠打",
        default = 0,
    )

    sacrifice_fly = models.PositiveSmallIntegerField(
        verbose_name = "犠飛",
        default = 0,
    )

    stolen_base = models.PositiveSmallIntegerField(
        verbose_name = "盗塁",
        default = 0,
    )

    grounded_into_double_play = models.PositiveSmallIntegerField(
        verbose_name = "併殺",
        default = 0,
    )

    error = models.PositiveSmallIntegerField(
        verbose_name = "失策",
        default = 0,
    )

    created_at = models.DateTimeField(
        verbose_name = "登録日",
        auto_now_add = True,
    )

    updated_at = models.DateTimeField(
        verbose_name = "更新日",
        auto_now = True,
    )

    class Meta:
        verbose_name = "打者一覧"
        verbose_name_plural = "打者成績"