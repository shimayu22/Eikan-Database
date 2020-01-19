from django.db import models


class ModelSettings(models.Model):
    
    is_used_limit_choices_to = models.BooleanField(
        verbose_name="過去の試合を修正する",
        default=False,
    )

    class Meta:
        verbose_name = "設定"
        verbose_name_plural = "設定"
