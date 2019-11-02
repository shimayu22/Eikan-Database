from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.
class Players(models.Model):

    # TODO: ポジションを作成する
    POSITION_CHOICES = (
        (0, "選択"),
        (1, "投"),
        (2, "捕"),
    )

    admission_year = models.IntegerField(
        verbose_name = "入学年度",
        validators = [MinValueValidator(1939)],
        # TODO: 一つ前のレコードの年度をdefaultにしたい
    )

    name = models.CharField(
        verbose_name = "名前",
        max_length = 6,
    )

    position = models.IntegerField(
        verbose_name = "守備位置",
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
        auto_now_add = True,
    )

    def __str__(self):
        return str(self.admission_year) + " : " + self.name
    

    class Meta:
        verbose_name_plural = "選手情報"