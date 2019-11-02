from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator

from eikan.models import Games,Players

# Create your models here.
class Pitcher_results(models.Model):
    game_id = models.ForeignKey(
        Games,
        on_delete=models.CASCADE,
    )

    player_id = models.ForeignKey(
        Players,
        on_delete=models.CASCADE,
        # TODO: 試合がある年度に在籍している選手だけ表示したい
        # TODO: 投手だけ表示したい
    )

    # TODO: 入力項目としては不要か
    game = models.IntegerField(
        verbose_name = "登板数",
        validators = [MinValueValidator(1)],
        default = 1,
    )

    # TODO: boolの方がよい？
    games_started = models.IntegerField(
        verbose_name = "先発登板",
        validators = [MinValueValidator(0)],
        default = 0,
    )

    innings_pitched = models.FloatField(
        verbose_name = "イニング",
        validators = [MinValueValidator(0)],
        default = 0,
    )

    total_batters_faced = models.IntegerField(
        verbose_name = "対戦打者",
        validators = [MinValueValidator(0)],
        default = 0,
    )

    number_of_pitch = models.IntegerField(
        verbose_name = "投球数",
        validators = [MinValueValidator(0)],
        default = 0,
    )

    hit = models.IntegerField(
        verbose_name = "被安打",
        validators = [MinValueValidator(0)],
        default = 0,
    )

    strike_out = models.IntegerField(
        verbose_name = "三振",
        validators = [MinValueValidator(0)],
        default = 0,
    )

    bases_on_balls = models.IntegerField(
        verbose_name = "四球",
        validators = [MinValueValidator(0)],
        default = 0,
    )

    hit_by_pitch = models.IntegerField(
        verbose_name = "死球",
        validators = [MinValueValidator(0)],
        default = 0,
    )

    run = models.IntegerField(
        verbose_name = "失点",
        validators = [MinValueValidator(0)],
        default = 0,
    )

    earned_run = models.IntegerField(
        verbose_name = "自責点",
        validators = [MinValueValidator(0)],
        default = 0,
    )

    wild_pitch = models.IntegerField(
        verbose_name = "暴投",
        validators = [MinValueValidator(0)],
        default = 0,
    )

    home_run = models.IntegerField(
        verbose_name = "本塁打",
        validators = [MinValueValidator(0)],
        default = 0,
    )

    sacrifice_bunt = models.IntegerField(
        verbose_name = "犠打",
        validators = [MinValueValidator(0)],
        default = 0,
    )

    sacrifice_fly = models.IntegerField(
        verbose_name = "犠飛",
        validators = [MinValueValidator(0)],
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
        return str(self.player_id) + " : " + str(self.game_id)
    

    class Meta:
        verbose_name_plural = "投手成績"