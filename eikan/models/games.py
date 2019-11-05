from django.db import models

from eikan.models.teams import Teams

# Create your models here.
class Games(models.Model):

    COMPETITON_CHOICES = (
        ('','選択'),
        (1,'練習試合'),
        (2,'県大会'),
        (3,'地区大会'),
        (4,'甲子園'),
        (5,'センバツ'),
    )

    ROUND_CHOICES = (
        ('','選択'),
        (1,'練習試合'),
        (2,'1回戦'),
        (3,'2回戦'),
        (4,'3回戦'),
        (5,'4回戦'),
        (6,'準々決勝'),
        (7,'準決勝'),
        (8,'決勝'),
    )

    RESULT_CHOICES = (
        ('', "選択"),
        (1, "勝"),
        (2, "負"),
        (3, "分"),
    )

    LANK_CHOICES = (
        ('','選択'),
        (1,'弱小'),
        (2,'そこそこ'),
        (3,'中堅'),
        (4,'強豪'),
        (5,'名門'),
    )

    team_id = models.ForeignKey(
        Teams,
        on_delete=models.CASCADE
    )

    competition_type = models.PositiveSmallIntegerField(
        verbose_name = "大会",
        choices = COMPETITON_CHOICES,
        default = 0,
    )

    competiton_round = models.PositiveSmallIntegerField(
        verbose_name = "回戦",
        choices = ROUND_CHOICES,
        default = 0
    )

    result = models.PositiveSmallIntegerField(
        verbose_name = "勝敗",
        choices = RESULT_CHOICES,
        default = 0,
    )

    score = models.PositiveSmallIntegerField(
        verbose_name = "得点",
        default = 0,
    )

    run = models.PositiveSmallIntegerField(
        verbose_name = "失点",
        default = 0,
    )

    lank = models.PositiveSmallIntegerField(
        verbose_name = "ランク",
        choices = LANK_CHOICES,
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

    def __str__(self):
        return f'{self.team_id}'
    

    class Meta:
        verbose_name = "試合情報"
        verbose_name_plural = "試合情報"