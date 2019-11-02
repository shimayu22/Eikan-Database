from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.
class Teams(models.Model):

    PERIOD_CHOICES = (
        (0, "選択"),
        (1, "夏"),
        (2, "秋"),
    )

    # TODO: 49代表を作成する
    PREFECTURE_CHOICES = (
        (0, "選択"),
        (1, "北北海道"),
        (2, "南北海道"),
    )

    # TODO: 育成方針を作成する
    POLICY_CHOICES = (
        (0, "選択"),
        (1, "おまかせ"),
        (2, "打撃"),
    )

    year = models.IntegerField(
        verbose_name = "年度",
        validators = [MinValueValidator(1941)],
        # TODO: 一つ前のレコードの年度をdefaultにしたい
    )

    period = models.IntegerField(
        verbose_name = "期間",
        choices = PERIOD_CHOICES,
        default = 0,
    )

    prefecture = models.IntegerField(
        verbose_name = "都道府県",
        choices = PREFECTURE_CHOICES,
        default = 0,
    )

    training_policy = models.IntegerField(
        verbose_name = "育成方針",
        choices = POLICY_CHOICES,
        default = 0,
    )

    draft_nomination = models.IntegerField(
        verbose_name = "指名人数",
        validators = [MinValueValidator(0),
                      MaxValueValidator(5)],
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
        return str(self.year) + " : " + str(self.period) + " : " + str(self.prefecture)
        # TODO: スマートな表示方法に変更したい

    class Meta:
        verbose_name_plural = "チーム情報"