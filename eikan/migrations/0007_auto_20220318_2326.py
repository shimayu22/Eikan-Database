# Generated by Django 2.2.27 on 2022-03-18 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eikan', '0006_players_is_two_way'),
    ]

    operations = [
        migrations.AddField(
            model_name='games',
            name='mamono_score',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='魔物使用得点'),
        ),
        migrations.AddField(
            model_name='teamtotalresults',
            name='mamono_score',
            field=models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='魔物使用得点'),
        ),
    ]
