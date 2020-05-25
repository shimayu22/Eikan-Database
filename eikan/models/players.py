from django.core.validators import MinValueValidator
from django.db import models
from eikan.model_manager import DefaultValueExtractor as d
from eikan.model_manager import SavedValueExtractor as s


class Players(models.Model):

    POSITION_CHOICES = (
        ('', '選択'),
        (1, '投'),
        (2, '捕'),
        (3, '一'),
        (4, '二'),
        (5, '三'),
        (6, '遊'),
        (7, '外'),
    )

    admission_year = models.PositiveSmallIntegerField(
        verbose_name="入学年度",
        validators=[MinValueValidator(1939)],
        default=d.create_default_year_for_players,
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

    def save(self, *args, **kwargs):
        self.is_pitcher = s.update_is_pitcher(
            self, self.position, self.is_pitched)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.admission_year}:{self.name}({self.POSITION_CHOICES[self.position][1]})'

    class Meta:
        verbose_name = "選手情報"
        verbose_name_plural = "(2)選手情報"
        ordering = ['admission_year', 'position']
        constraints = [models.UniqueConstraint(fields=['admission_year', 'name'], name='unique_player'), ]
