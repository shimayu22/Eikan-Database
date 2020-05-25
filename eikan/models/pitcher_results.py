from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from eikan.models import Games, Players
from eikan.model_manager import DefaultValueExtractor as d


class PitcherResults(models.Model):

    game_id = models.ForeignKey(
        Games,
        on_delete=models.CASCADE,
    )

    player_id = models.ForeignKey(
        Players,
        on_delete=models.CASCADE,
        verbose_name="選手",
        limit_choices_to=d.select_display_pitchers,
    )

    games_started = models.BooleanField(
        verbose_name="先発登板",
        default=False,
    )

    innings_pitched = models.PositiveSmallIntegerField(
        verbose_name="イニング",
        validators=[MinValueValidator(0), MaxValueValidator(15)],
        default=0,
    )

    innings_pitched_fraction = models.PositiveSmallIntegerField(
        verbose_name="/3",
        validators=[MinValueValidator(0), MaxValueValidator(2)],
        default=0,
    )

    number_of_pitch = models.PositiveSmallIntegerField(
        verbose_name="投球数",
        default=0,
    )

    total_batters_faced = models.PositiveSmallIntegerField(
        verbose_name="対戦打者",
        default=0,
    )

    hit = models.PositiveSmallIntegerField(
        verbose_name="被安打",
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

    run = models.PositiveSmallIntegerField(
        verbose_name="失点",
        default=0,
    )

    earned_run = models.PositiveSmallIntegerField(
        verbose_name="自責点",
        default=0,
    )

    wild_pitch = models.PositiveSmallIntegerField(
        verbose_name="暴投",
        default=0,
    )

    home_run = models.PositiveSmallIntegerField(
        verbose_name="本塁打",
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
        verbose_name = "投手一覧"
        verbose_name_plural = "投手成績"
        constraints = [models.UniqueConstraint(fields=['game_id', 'player_id'], name='unique_pitcherresult'), ]
