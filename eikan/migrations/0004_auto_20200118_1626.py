# Generated by Django 2.2.6 on 2020-01-18 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eikan', '0003_auto_20200115_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='fieldertotalresults',
            name='br',
            field=models.DecimalField(decimal_places=1, default=0.0, editable=False, max_digits=4, verbose_name='BR'),
        ),
        migrations.AddField(
            model_name='fieldertotalresults',
            name='woba',
            field=models.DecimalField(decimal_places=3, default=0.0, editable=False, max_digits=4, verbose_name='wOBA'),
        ),
    ]