from django.db import models
from eikan.models import Players

class PlayersFielder(model.Model):

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

    total_bases = models.PositiveIntegerField(
        verbose_name="塁打",
        default=0,
        editable=False,     
    )

    slg = models.DecimalField(
        verbose_name="長打率",
        max_digits=4,
        decimal_places=3,
        default=0.000,
        editable=False,
    )

    obp = models.DecimalField(
        verbose_name="出塁率",
        max_digits=4,
        decimal_places=3,
        default=0.000,
        editable=False,
    )

    gpa = models.DecimalField(
        verbose_name="GPA",
        max_digits=4,
        decimal_places=3,
        default=0.000,
        editable=False,
    )

    batting_average = models.DecimalField(
        verbose_name="打率",
        max_digits=4,
        decimal_places=3,
        default=0.000,
        editable=False,
    )

    bbhp_percent = models.DecimalField(
        verbose_name="BBHP%",
        max_digits=4,
        decimal_places=3,
        default=0.000,
        editable=False,
    )

    isod = models.DecimalField(
        verbose_name="IsoD",
        max_digits=4,
        decimal_places=3,
        default=0.000,
        editable=False,
    )

    isop = models.DecimalField(
        verbose_name="IsoP",
        max_digits=4,
        decimal_places=3,
        default=0.000,
        editable=False,
    )

    bbhp_k = models.DecimalField(
        verbose_name="BBHP/K",
        max_digits=4,
        decimal_places=3,
        default=0.00,
        editable=False,
    )

    p_s = models.DecimalField(
        verbose_name="P-S",
        max_digits=6,
        decimal_places=3,
        default=0.000,
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
        verbose_name = "打者総合成績"
        verbose_name_plural = "打者総合成績"