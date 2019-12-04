from django.db import models
from eikan.models import Teams

class TeamsTotalResults(models.Model):

    RANK_CHOICES = (
        ('','選択'),
        (1,'弱小'),
        (2,'そこそこ'),
        (3,'中堅'),
        (4,'強豪'),
        (5,'名門'),
    )

    team_id = models.ForeignKey(
        Teams,
        on_delete=models.CASCADE,
        verbose_name="チーム",
        editable=False,
    )

    year = models.PositiveSmallIntegerField(
        verbose_name="年度",
        default=0,
        editable=False,
    )

    period = models.PositiveSmallIntegerField(
        verbose_name="期間",
        default=0,
        editable=False,
    )

    total_win = models.PositiveSmallIntegerField(
        verbose_name="勝",
        default=0,
        editable=False,
    )

    total_lose = models.PositiveSmallIntegerField(
        verbose_name="負",
        default=0,
        editable=False,
    )

    total_draw = models.PositiveSmallIntegerField(
        verbose_name="分",
        default=0,
        editable=False,
    )

    score = models.PositiveSmallIntegerField(
        verbose_name="得点",
        default=0,
        editable=False,
    )

    run = models.PositiveSmallIntegerField(
        verbose_name="失点",
        default=0,
        editable=False,
    )

    score_difference = models.IntegerField(
        verbose_name="得失点差",
        default=0,
        editable=False,
    )

    rank = models.PositiveSmallIntegerField(
        verbose_name="ランク",
        default=0,
        choices=RANK_CHOICES,
        editable=False,
    )

    batting_average = models.DecimalField(
        verbose_name="打率",
        max_digits=4,
        decimal_places=3,
        default=0.000,
        editable=False,
    )

    ops = models.DecimalField(
        verbose_name="OPS",
        max_digits=4,
        decimal_places=3,
        default=0.000,
        editable=False,
    )

    hr = models.PositiveSmallIntegerField(
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

    der = models.DecimalField(
        verbose_name="DER",
        max_digits=4,
        decimal_places=3,
        default=0.000,
        editable=False,
    )

    remark = models.CharField(
        verbose_name="備考",
        max_length=100,
        blank=True,
        null=True,
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
        return f'{self.team_id}'

    class Meta:
        verbose_name = "チーム総合成績"
        verbose_name_plural = "チーム総合成績"