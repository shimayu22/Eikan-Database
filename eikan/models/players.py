from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.
class Players(models.Model):

    POSITION_CHOICES = (
        ('','選択'),
        (1,'投'),
        (2,'捕'),
        (3,'一'),
        (4,'二'),
        (5,'三'),
        (6,'遊'),
        (7,'外'),
    )

    admission_year = models.PositiveSmallIntegerField(
        verbose_name = "入学年度",
        validators = [MinValueValidator(1939)],
        default = lambda: Players.objects.latest('pk').admission_year \
                          if Players.objects.all() else 1939,
    )

    name = models.CharField(
        verbose_name = "名前",
        max_length = 6,
    )

    position = models.PositiveSmallIntegerField(
        verbose_name = "メインポジション",
        choices = POSITION_CHOICES,
        default = 0,
    )

    remark = models.CharField(
        verbose_name = "備考",
        max_length = 100,
        blank = True,
        null = True,
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
        return f'{self.admission_year}:{self.name}({self.POSITION_CHOICES[self.position][1]})'

    class Meta:
        verbose_name = "選手情報"
        verbose_name_plural = "選手情報"