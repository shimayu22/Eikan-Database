from django.db import models
from eikan.models import Teams

# Create your models here.


def default_team_id():
    return Teams.objects.latest('pk').id \
        if Teams.objects.count() > 0 else 0


def default_team_rank():
    return Games.objects.latest('pk').rank \
        if Games.objects.count() > 0 else 0


class Games(models.Model):

    COMPETITON_CHOICES = (
        ('', '選択'),
        (1, '練習試合'),
        (2, '県大会'),
        (3, '地区大会'),
        (4, '甲子園'),
        (5, 'センバツ'),
    )

    ROUND_CHOICES = (
        ('', '選択'),
        (1, '練習試合'),
        (2, '1回戦'),
        (3, '2回戦'),
        (4, '3回戦'),
        (5, '4回戦'),
        (6, '準々決勝'),
        (7, '準決勝'),
        (8, '決勝'),
    )

    RESULT_CHOICES = (
        ('', "選択"),
        (1, "勝"),
        (2, "負"),
        (3, "分"),
    )

    RANK_CHOICES = (
        ('', '選択'),
        (1, '弱小'),
        (2, 'そこそこ'),
        (3, '中堅'),
        (4, '強豪'),
        (5, '名門'),
    )

    team_id = models.ForeignKey(
        Teams,
        on_delete=models.CASCADE,
        default=default_team_id,
        verbose_name="チーム",
    )

    competition_type = models.PositiveSmallIntegerField(
        verbose_name="大会",
        choices=COMPETITON_CHOICES,
        default=0,
    )

    competiton_round = models.PositiveSmallIntegerField(
        verbose_name="回戦",
        choices=ROUND_CHOICES,
        default=0
    )

    result = models.PositiveSmallIntegerField(
        verbose_name="勝敗",
        choices=RESULT_CHOICES,
        default=0,
        editable=False,
    )

    score = models.PositiveSmallIntegerField(
        verbose_name="得点",
        default=0,
    )

    run = models.PositiveSmallIntegerField(
        verbose_name="失点",
        default=0,
    )

    rank = models.PositiveSmallIntegerField(
        verbose_name="ランク",
        choices=RANK_CHOICES,
        default=default_team_rank,
    )

    created_at = models.DateTimeField(
        verbose_name="登録日",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        verbose_name="更新日",
        auto_now=True,
    )

    def save(self, *args, **kwargs):
        if self.score > self.run:
            self.result = 1
        elif self.score < self.run:
            self.result = 2
        else:
            self.result = 3
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.team_id}'

    class Meta:
        verbose_name = "試合情報"
        verbose_name_plural = "(1)試合情報"
