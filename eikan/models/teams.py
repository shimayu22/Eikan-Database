from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from eikan.model_manager import DefaultValueExtractor as d


class Teams(models.Model):

    PERIOD_CHOICES = (
        ('', "選択"),
        (1, "夏"),
        (2, "秋"),
    )

    PREFECTURE_CHOICES = (
        ('', '選択'),
        (1, '北北海道'),
        (2, '南北海道'),
        (3, '青森'),
        (4, '岩手'),
        (5, '宮城'),
        (6, '秋田'),
        (7, '山形'),
        (8, '福島'),
        (9, '茨城'),
        (10, '栃木'),
        (11, '群馬'),
        (12, '埼玉'),
        (13, '千葉'),
        (14, '神奈川'),
        (15, '山梨'),
        (16, '東東京'),
        (17, '西東京'),
        (18, '新潟'),
        (19, '富山'),
        (20, '石川'),
        (21, '福井'),
        (22, '長野'),
        (23, '岐阜'),
        (24, '静岡'),
        (25, '愛知'),
        (26, '三重'),
        (27, '滋賀'),
        (28, '京都'),
        (29, '大阪'),
        (30, '兵庫'),
        (31, '奈良'),
        (32, '和歌山'),
        (33, '鳥取'),
        (34, '島根'),
        (35, '岡山'),
        (36, '広島'),
        (37, '山口'),
        (38, '徳島'),
        (39, '香川'),
        (40, '愛媛'),
        (41, '高知'),
        (42, '福岡'),
        (43, '佐賀'),
        (44, '長崎'),
        (45, '熊本'),
        (46, '大分'),
        (47, '宮崎'),
        (48, '鹿児島'),
        (49, '沖縄'),
    )

    POLICY_CHOICES = (
        ('', '選択'),
        (1, 'バランス'),
        (2, '打撃力'),
        (3, '機動力'),
        (4, '守備・投手'),
    )

    year = models.PositiveSmallIntegerField(
        verbose_name="年度",
        validators=[MinValueValidator(1941)],
        default=d.create_default_year_for_teams,
    )

    period = models.PositiveSmallIntegerField(
        verbose_name="期間",
        choices=PERIOD_CHOICES,
        default=d.create_default_period,
    )

    prefecture = models.PositiveSmallIntegerField(
        verbose_name="都道府県",
        choices=PREFECTURE_CHOICES,
        default=d.create_default_prefecture,
    )

    training_policy = models.PositiveSmallIntegerField(
        verbose_name="育成方針",
        choices=POLICY_CHOICES,
        default=0,
    )

    draft_nomination = models.PositiveSmallIntegerField(
        verbose_name="指名人数",
        validators=[MinValueValidator(0),
                    MaxValueValidator(5)],
        default=0,
    )

    remark = models.CharField(
        verbose_name="備考",
        max_length=100,
        blank=True,
        null=True,
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
        return f'{self.year}:{self.PERIOD_CHOICES[self.period][1]}:{self.PREFECTURE_CHOICES[self.prefecture][1]}'

    class Meta:
        verbose_name = "チーム情報"
        verbose_name_plural = "(3)チーム情報"
        # 試合情報で入力しやすいように追加
        ordering = ['-year', '-period']
        constraints = [models.UniqueConstraint(fields=['year', 'period'], name='unique_team'), ]
