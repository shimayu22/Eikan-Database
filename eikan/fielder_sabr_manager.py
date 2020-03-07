from django.db import models
from eikan.models import FielderResults, FielderTotalResults
from eikan.calculate_sabr import CalculateFielderSabr as f


class FielderSabrFormatter:

    def __init__(self):
        self

    def update_fielder_total_results(
            self,
            fielder_results,
            fielder_total_results):
        fielder_total_results.at_bat = fielder_results['at_bat__sum']
        fielder_total_results.run = fielder_results['run__sum']
        fielder_total_results.hit = fielder_results['hit__sum']
        fielder_total_results.two_base = fielder_results['two_base__sum']
        fielder_total_results.three_base = fielder_results['three_base__sum']
        fielder_total_results.home_run = fielder_results['home_run__sum']
        fielder_total_results.run_batted_in = fielder_results['run_batted_in__sum']
        fielder_total_results.strike_out = fielder_results['strike_out__sum']
        fielder_total_results.bb_hbp = fielder_results['bb_hbp__sum']
        fielder_total_results.sacrifice_bunt = fielder_results['sacrifice_bunt__sum']
        fielder_total_results.stolen_base = fielder_results['stolen_base__sum']
        fielder_total_results.grounded_into_double_play = fielder_results[
            'grounded_into_double_play__sum']
        fielder_total_results.error = fielder_results['error__sum']
        fielder_total_results.total_bases = f.total_bases(
            self,
            fielder_results['hit__sum'],
            fielder_results['two_base__sum'],
            fielder_results['three_base__sum'],
            fielder_results['home_run__sum'])
        fielder_total_results.obp = f.on_base_percentage(
            self,
            fielder_results['at_bat__sum'],
            fielder_results['bb_hbp__sum'],
            fielder_results['hit__sum'])
        fielder_total_results.slg = f.slugging_percentage(
            self,
            fielder_results['at_bat__sum'],
            fielder_total_results.total_bases)
        fielder_total_results.ops = f.on_base_plus_slugging(
            self,
            fielder_total_results.obp,
            fielder_total_results.slg)
        fielder_total_results.br = f.batting_runs(
            self,
            fielder_results['hit__sum'],
            fielder_results['two_base__sum'],
            fielder_results['three_base__sum'],
            fielder_results['home_run__sum'],
            fielder_results['bb_hbp__sum'],
            fielder_results['at_bat__sum']
        )
        fielder_total_results.woba = f.weighted_on_base_average(
            self,
            fielder_results['hit__sum'],
            fielder_results['two_base__sum'],
            fielder_results['three_base__sum'],
            fielder_results['home_run__sum'],
            fielder_results['bb_hbp__sum'],
            fielder_results['at_bat__sum']
        )
        fielder_total_results.gpa = f.gross_production_average(
            self,
            fielder_total_results.obp,
            fielder_total_results.slg)
        fielder_total_results.batting_average = f.batting_average(
            self,
            fielder_results['at_bat__sum'],
            fielder_results['hit__sum'])
        fielder_total_results.bbhp_percent = f.bb_hp_percentage(
            self,
            fielder_results['at_bat__sum'],
            fielder_results['bb_hbp__sum'],
            fielder_results['sacrifice_bunt__sum'])
        fielder_total_results.isod = f.isolated_discipline(
            self,
            fielder_total_results.obp,
            fielder_total_results.batting_average)
        fielder_total_results.isop = f.isolated_power(
            self,
            fielder_total_results.slg,
            fielder_total_results.batting_average)
        fielder_total_results.bbhp_k = f.bb_hbp_per_so(
            self,
            fielder_results['strike_out__sum'],
            fielder_results['bb_hbp__sum'])
        fielder_total_results.p_s = f.power_speed_number(
            self,
            fielder_results['home_run__sum'],
            fielder_results['stolen_base__sum'])

        return fielder_total_results

    def tally_from_player_all_results(self):
        fielder_results = FielderResults.objects.select_related('player_id').filter(
            player_id=self.player_id).aggregate(
            models.Sum('at_bat'),
            models.Sum('run'),
            models.Sum('hit'),
            models.Sum('two_base'),
            models.Sum('three_base'),
            models.Sum('home_run'),
            models.Sum('run_batted_in'),
            models.Sum('strike_out'),
            models.Sum('bb_hbp'),
            models.Sum('sacrifice_bunt'),
            models.Sum('stolen_base'),
            models.Sum('grounded_into_double_play'),
            models.Sum('error'))

        return fielder_results

    def tally_from_player_results_by_year(self):
        fielder_results = FielderResults.objects.select_related(
            'game_id__team_id',
            'game_id',
            'player_id').filter(
            player_id=self.player_id).values(
            'game_id__team_id__year').annotate(
            at_bat__sum=models.Sum('at_bat'),
            run__sum=models.Sum('run'),
            hit__sum=models.Sum('hit'),
            two_base__sum=models.Sum('two_base'),
            three_base__sum=models.Sum('three_base'),
            home_run__sum=models.Sum('home_run'),
            run_batted_in__sum=models.Sum('run_batted_in'),
            strike_out__sum=models.Sum('strike_out'),
            bb_hbp__sum=models.Sum('bb_hbp'),
            sacrifice_bunt__sum=models.Sum('sacrifice_bunt'),
            stolen_base__sum=models.Sum('stolen_base'),
            grounded_into_double_play__sum=models.Sum(
                'grounded_into_double_play'),
            error__sum=models.Sum('error')).order_by('-game_id__team_id__year')

        return fielder_results

    def tally_from_player_results_of_team(self):
        fielder_results = FielderResults.objects.select_related(
            'game_id__team_id',
            'player_id').filter(
            game_id__team_id=self.team_id).values(
            'player_id').annotate(
            at_bat__sum=models.Sum('at_bat'),
            run__sum=models.Sum('run'),
            hit__sum=models.Sum('hit'),
            two_base__sum=models.Sum('two_base'),
            three_base__sum=models.Sum('three_base'),
            home_run__sum=models.Sum('home_run'),
            run_batted_in__sum=models.Sum('run_batted_in'),
            strike_out__sum=models.Sum('strike_out'),
            bb_hbp__sum=models.Sum('bb_hbp'),
            sacrifice_bunt__sum=models.Sum('sacrifice_bunt'),
            stolen_base__sum=models.Sum('stolen_base'),
            grounded_into_double_play__sum=models.Sum(
                'grounded_into_double_play'),
            error__sum=models.Sum('error')).order_by('player_id')

        return fielder_results

    # FielderTotalResults更新用メソッド
    def update_total_results(self, player_id):
        self.player_id = player_id
        fielder_total_results = FielderTotalResults.objects.select_related(
            'player_id').get(player_id=self.player_id)
        fielder_results = self.tally_from_player_all_results()
        f = self.update_fielder_total_results(
            fielder_results, fielder_total_results)
        f.save()

    # 打者詳細画面用にデータを取得するメソッド
    def create_sabr_from_results_by_year(self, player_id):
        self.player_id = player_id
        fielder_total_results = FielderTotalResults.objects.select_related(
            'player_id').get(player_id=self.player_id)
        fielder_results = self.tally_from_player_results_by_year()
        fielder_total_results_list = []

        for result in fielder_results:
            f = self.update_fielder_total_results(
                result, fielder_total_results)
            f.year = result['game_id__team_id__year']
            fielder_total_results_list.append(f)

        return fielder_total_results_list

    # チーム詳細画面用にデータを取得するメソッド
    def create_sabr_from_results_of_team(self, team_id):
        self.team_id = team_id
        fielder_results = self.tally_from_player_results_of_team()
        player_list = []

        for player in fielder_results:
            player_list.append(player['player_id'])

        fielder_total_results = FielderTotalResults.objects.select_related(
            'player_id').filter(player_id__in=player_list).order_by('player_id')
        fielder_total_results_list = []

        for result, total_results in zip(
                fielder_results, fielder_total_results):
            f = self.update_fielder_total_results(
                result, total_results)
            fielder_total_results_list.append(f)

        return fielder_total_results_list
