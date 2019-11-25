from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from eikan.models import Teams

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
        verbose_name="入学年度",
        validators=[MinValueValidator(1939)],
        default=Teams.objects.latest('pk').year \
                 if Teams.objects.count() > 0 else 1939,
    )

    name = models.CharField(
        verbose_name="名前",
        max_length=6,
    )

    position = models.PositiveSmallIntegerField(
        verbose_name="メインポジション",
        choices=POSITION_CHOICES,
        default=0,
    )

    is_pitched = models.BooleanField(
        verbose_name="野手登板",
        default=False,
    )

    is_ob = models.BooleanField(
        verbose_name="OB",
        default=False,
    )

    is_active = models.BooleanField(
        verbose_name="現役",
        default=False,
    )

    is_genius = models.BooleanField(
        verbose_name="天才",
        default=False,
    )

    remark = models.CharField(
        verbose_name="備考",
        max_length=100,
        blank=True,
        null=True,
    )

    is_pitcher = models.BooleanField(
        verbose_name="投手",
        default=False,
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

    # 以下編集不可

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

    # 以下投手
    era = models.DecimalField(
        verbose_name="防御率",
        max_digits=5,
        decimal_places=2,
        default=0.00,
        editable=False,
    )

    ura = models.DecimalField(
        verbose_name="失点率",
        max_digits=5,
        decimal_places=2,
        default=0.00,
        editable=False,
    )

    whip = models.DecimalField(
        verbose_name="WHIP",
        max_digits=3,
        decimal_places=2,
        default=0.00,
        editable=False,
    )

    k_bbhp = models.DecimalField(
        verbose_name="K/BBHP",
        max_digits=4,
        decimal_places=2,
        default=0.00,
        editable=False,
    )

    k_9 = models.DecimalField(
        verbose_name="K/9",
        max_digits=4,
        decimal_places=2,
        default=0.00,
        editable=False,
    )

    k_percent = models.DecimalField(
        verbose_name="K%",
        max_digits=4,
        decimal_places=2,
        default=0.00,
        editable=False,
    )

    bbhp_9 = models.DecimalField(
        verbose_name="BBHP/9",
        max_digits=4,
        decimal_places=2,
        default=0.00,
        editable=False,
    )

    p_bbhp_percent = models.DecimalField(
        verbose_name="BBHP%",
        max_digits=4,
        decimal_places=2,
        default=0.00,
        editable=False,
    )

    hr_9 = models.DecimalField(
        verbose_name="HR/9",
        max_digits=3,
        decimal_places=2,
        default=0.00,
        editable=False,
    )

    hr_percent = models.DecimalField(
        verbose_name="HR%",
        max_digits=4,
        decimal_places=2,
        default=0.00,
        editable=False,
    )

    lob_percent = models.DecimalField(
        verbose_name="LOB%",
        max_digits=4,
        decimal_places=2,
        default=0.00,
        editable=False,
    )

    p_ip = models.DecimalField(
        verbose_name="P/IP",
        max_digits=4,
        decimal_places=2,
        default=0.00,
        editable=False,
    )

    def save(self, *args, **kwargs):
        if self.position == 1 or self.is_pitched:
            self.is_pitcher = True
        elif self.position > 1 and not self.is_pitched:
            self.is_pitcher = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.admission_year}:{self.name}({self.POSITION_CHOICES[self.position][1]})'

    class Meta:
        verbose_name = "選手情報"
        verbose_name_plural = "選手情報"
        ordering = ['admission_year', 'position']
