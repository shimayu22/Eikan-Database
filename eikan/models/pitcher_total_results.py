from django.db import models
from eikan.models import Players

class PitcherTotalResults(models.Model):

    player_id = models.ForeignKey(
        Players,
        on_delete=models.CASCADE,
        verbose_name="選手",
        editable=False,
    )

    games = models.PositiveSmallIntegerField(
        verbose_name="登板",
        default=0,
        editable=False,
    )

    games_started = models.PositiveSmallIntegerField(
        verbose_name="先発登板",
        default=0,
        editable=False,
    )

    innings_pitched = models.FloatField(
        verbose_name="イニング",
        default=0.0,
        editable=False,
    )

    number_of_pitch = models.PositiveSmallIntegerField(
        verbose_name="投球数",
        default=0,
        editable=False,
    )
    
    total_batters_faced = models.PositiveSmallIntegerField(
        verbose_name="対戦打者",
        default=0,
        editable=False,
    )

    hit = models.PositiveSmallIntegerField(
        verbose_name="被安打",
        default=0,
        editable=False,
    )

    strike_out = models.PositiveSmallIntegerField(
        verbose_name="三振",
        default=0,
        editable=False,
    )

    bb_hbp = models.PositiveSmallIntegerField(
        verbose_name="四死球",
        default=0,
        editable=False,
    )

    run = models.PositiveSmallIntegerField(
        verbose_name="失点",
        default=0,
        editable=False,
    )

    earned_run = models.PositiveSmallIntegerField(
        verbose_name="自責点",
        default=0,
        editable=False,
    )

    wild_pitch = models.PositiveSmallIntegerField(
        verbose_name="暴投",
        default=0,
        editable=False,
    )

    home_run = models.PositiveSmallIntegerField(
        verbose_name="本塁打",
        default=0,
        editable=False,
    )

    era = models.DecimalField(
        verbose_name="防御率",
        max_digits=5,
        decimal_places=2,
        default=0.00,
        editable=False,
    )

    ura = models.DecimalField(
        verbose_name="失点率",
        max_digits=5,
        decimal_places=2,
        default=0.00,
        editable=False,
    )

    whip = models.DecimalField(
        verbose_name="WHIP",
        max_digits=3,
        decimal_places=2,
        default=0.00,
        editable=False,
    )

    k_bbhp = models.DecimalField(
        verbose_name="K/BBHP",
        max_digits=4,
        decimal_places=2,
        default=0.00,
        editable=False,
    )

    k_9 = models.DecimalField(
        verbose_name="K/9",
        max_digits=4,
        decimal_places=2,
        default=0.00,
        editable=False,
    )

    k_percent = models.DecimalField(
        verbose_name="K%",
        max_digits=4,
        decimal_places=2,
        default=0.00,
        editable=False,
    )

    bbhp_9 = models.DecimalField(
        verbose_name="BBHP/9",
        max_digits=4,
        decimal_places=2,
        default=0.00,
        editable=False,
    )

    p_bbhp_percent = models.DecimalField(
        verbose_name="BBHP%",
        max_digits=4,
        decimal_places=2,
        default=0.00,
        editable=False,
    )

    hr_9 = models.DecimalField(
        verbose_name="HR/9",
        max_digits=3,
        decimal_places=2,
        default=0.00,
        editable=False,
    )

    hr_percent = models.DecimalField(
        verbose_name="HR%",
        max_digits=4,
        decimal_places=2,
        default=0.00,
        editable=False,
    )

    lob_percent = models.DecimalField(
        verbose_name="LOB%",
        max_digits=4,
        decimal_places=2,
        default=0.00,
        editable=False,
    )

    p_ip = models.DecimalField(
        verbose_name="P/IP",
        max_digits=4,
        decimal_places=2,
        default=0.00,
        editable=False,
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
        return f'{self.player_id}'

    class Meta:
        verbose_name = "投手総合成績"
        verbose_name_plural = "投手総合成績"