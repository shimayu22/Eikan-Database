# Generated by Django 2.2.6 on 2019-12-13 05:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eikan', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='games',
            options={'verbose_name': '試合情報', 'verbose_name_plural': '(1)試合情報'},
        ),
        migrations.AlterModelOptions(
            name='players',
            options={'ordering': ['admission_year', 'position'], 'verbose_name': '選手情報', 'verbose_name_plural': '(2)選手情報'},
        ),
        migrations.AlterModelOptions(
            name='teams',
            options={'ordering': ['-year', '-period'], 'verbose_name': 'チーム情報', 'verbose_name_plural': '(3)チーム情報'},
        ),
        migrations.RemoveField(
            model_name='teamstotalresults',
            name='period',
        ),
        migrations.RemoveField(
            model_name='teamstotalresults',
            name='rank',
        ),
        migrations.RemoveField(
            model_name='teamstotalresults',
            name='remark',
        ),
        migrations.RemoveField(
            model_name='teamstotalresults',
            name='year',
        ),
    ]
