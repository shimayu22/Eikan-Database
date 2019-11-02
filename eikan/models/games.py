from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator

from eikan.models.teams import Teams

# Create your models here.
class Games(models.Model):

    # TODO:大会種別を作成する
    COMPETITON_CHOICES = (
        (0, "選択"),
        (1, "甲子園"),
        # 練習試合も考慮
    )

    # TODO:n回戦を作成する
    ROUND_CHOICES = (
        (0, "選択"),
        (1, "1回戦"),
        ## 練習試合も考慮
    )

    RESULT_CHOICES = (
        (0, "選択"),
        (1, "勝"),
        (2, "負"),
        (3, "分"),
    )

    # TODO: ランクを作成する
    LANK_CHOICES = (
        (0, "選択"),
        (1, "そこそこ"),
    )

    team_id = models.ForeignKey(
        Teams,
        on_delete=models.CASCADE
    )

    competition_type = models.IntegerField(
        verbose_name = "大会",
        choices = COMPETITON_CHOICES,
        default = 0,
    )

    competiton_round = models.IntegerField(
        verbose_name = "回戦",
        choices = ROUND_CHOICES,
        default = 0
    )

    result = models.IntegerField(
        verbose_name = "勝敗",
        choices = RESULT_CHOICES,
        default = 0,
    )

    score = models.IntegerField(
        verbose_name = "得点",
        validators = [MinValueValidator(0)],
        default = 0,
    )

    run = models.IntegerField(
        verbose_name = "失点",
        validators = [MinValueValidator(0)],
        default = 0,
    )

    lank = models.IntegerField(
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
        auto_now_add = True,
    )

    def __str__(self):
        return ["","甲子園"][self.competition_type] + " : " + ["","1回戦"][self.competiton_round]
    

    class Meta:
        verbose_name_plural = "試合情報"