# Generated by Django 2.2.6 on 2020-05-25 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eikan', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelsettings',
            name='is_disable_auto_update',
            field=models.BooleanField(default=False, verbose_name='自動更新を停止する'),
        ),
    ]
