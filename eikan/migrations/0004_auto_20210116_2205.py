# Generated by Django 2.2.6 on 2021-01-16 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eikan', '0003_auto_20201013_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fieldertotalresults',
            name='bbhp_k',
            field=models.DecimalField(decimal_places=3, default=0.0, editable=False, max_digits=5, verbose_name='BBHP/K'),
        ),
    ]
