# Generated by Django 2.2.6 on 2019-12-02 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eikan', '0003_auto_20191202_0000'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayersPitcher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('games_started', models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='先発登板')),
                ('innings_pitched', models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='イニング')),
                ('total_batters_faced', models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='対戦打者')),
                ('number_of_pitch', models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='投球数')),
                ('hit', models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='被安打')),
                ('strike_out', models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='三振')),
                ('bb_hbp', models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='四死球')),
                ('run', models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='失点')),
                ('earned_run', models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='自責点')),
                ('wild_pitch', models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='暴投')),
                ('home_run', models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='本塁打')),
                ('era', models.DecimalField(decimal_places=2, default=0.0, editable=False, max_digits=5, verbose_name='防御率')),
                ('ura', models.DecimalField(decimal_places=2, default=0.0, editable=False, max_digits=5, verbose_name='失点率')),
                ('whip', models.DecimalField(decimal_places=2, default=0.0, editable=False, max_digits=3, verbose_name='WHIP')),
                ('k_bbhp', models.DecimalField(decimal_places=2, default=0.0, editable=False, max_digits=4, verbose_name='K/BBHP')),
                ('k_9', models.DecimalField(decimal_places=2, default=0.0, editable=False, max_digits=4, verbose_name='K/9')),
                ('k_percent', models.DecimalField(decimal_places=2, default=0.0, editable=False, max_digits=4, verbose_name='K%')),
                ('bbhp_9', models.DecimalField(decimal_places=2, default=0.0, editable=False, max_digits=4, verbose_name='BBHP/9')),
                ('p_bbhp_percent', models.DecimalField(decimal_places=2, default=0.0, editable=False, max_digits=4, verbose_name='BBHP%')),
                ('hr_9', models.DecimalField(decimal_places=2, default=0.0, editable=False, max_digits=3, verbose_name='HR/9')),
                ('hr_percent', models.DecimalField(decimal_places=2, default=0.0, editable=False, max_digits=4, verbose_name='HR%')),
                ('lob_percent', models.DecimalField(decimal_places=2, default=0.0, editable=False, max_digits=4, verbose_name='LOB%')),
                ('p_ip', models.DecimalField(decimal_places=2, default=0.0, editable=False, max_digits=4, verbose_name='P/IP')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='登録日')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日')),
                ('player_id', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='eikan.Players', verbose_name='選手')),
            ],
            options={
                'verbose_name_plural': '投手成績',
            },
        ),
        migrations.CreateModel(
            name='PlayersFielder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('at_bat', models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='打数')),
                ('run', models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='得点')),
                ('hit', models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='安打')),
                ('two_base', models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='二塁打')),
                ('three_base', models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='三塁打')),
                ('home_run', models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='本塁打')),
                ('run_batted_in', models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='打点')),
                ('strike_out', models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='三振')),
                ('bb_hbp', models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='四死球')),
                ('sacrifice_bunt', models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='犠打')),
                ('stolen_base', models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='盗塁')),
                ('grounded_into_double_play', models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='併殺')),
                ('error', models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='失策')),
                ('total_bases', models.PositiveIntegerField(default=0, editable=False, verbose_name='塁打')),
                ('slg', models.DecimalField(decimal_places=3, default=0.0, editable=False, max_digits=4, verbose_name='長打率')),
                ('obp', models.DecimalField(decimal_places=3, default=0.0, editable=False, max_digits=4, verbose_name='出塁率')),
                ('gpa', models.DecimalField(decimal_places=3, default=0.0, editable=False, max_digits=4, verbose_name='GPA')),
                ('batting_average', models.DecimalField(decimal_places=3, default=0.0, editable=False, max_digits=4, verbose_name='打率')),
                ('bbhp_percent', models.DecimalField(decimal_places=3, default=0.0, editable=False, max_digits=4, verbose_name='BBHP%')),
                ('isod', models.DecimalField(decimal_places=3, default=0.0, editable=False, max_digits=4, verbose_name='IsoD')),
                ('isop', models.DecimalField(decimal_places=3, default=0.0, editable=False, max_digits=4, verbose_name='IsoP')),
                ('bbhp_k', models.DecimalField(decimal_places=3, default=0.0, editable=False, max_digits=4, verbose_name='BBHP/K')),
                ('p_s', models.DecimalField(decimal_places=3, default=0.0, editable=False, max_digits=6, verbose_name='P-S')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='登録日')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日')),
                ('player_id', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='eikan.Players', verbose_name='選手')),
            ],
            options={
                'verbose_name': '打者総合成績',
                'verbose_name_plural': '打者総合成績',
            },
        ),
    ]
