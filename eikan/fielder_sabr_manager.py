"""打者成績に関する処理"""

from django.db import models
from eikan.models import FielderResults, FielderTotalResults, Teams, Players
from eikan.calculate_sabr import CalculateFielderSabr as f


class FielderSabrFormatter:
    """主にFielderResults,FielderTotalResultsを操作する"""

    def __init__(self):
        self

    def create_fielder_total_results(
            self,
            fielder_results: FielderResults) -> FielderTotalResults:
        """集計したFielderResultsをもとに更新用のFielderTotalResultsを作る

        Args:
            fielder_results (FielderResults):集計したFielderResults

        Returns:
            FielderTotalResults: 計算した指標を代入したFielderTotalResults

        Notes:
            セイバーメトリクスはここで計算する
        """
        fielder_total_results = FielderTotalResults.objects.select_related(
            'player_id').get(player_id=self.player_id)
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
            fielder_results['hit__sum'],
            fielder_results['two_base__sum'],
            fielder_results['three_base__sum'],
            fielder_results['home_run__sum'])
        fielder_total_results.slg = f.slugging_percentage(
            fielder_results['at_bat__sum'],
            fielder_total_results.total_bases)
        fielder_total_results.obp = f.on_base_percentage(
            fielder_results['at_bat__sum'],
            fielder_results['bb_hbp__sum'],
            fielder_results['hit__sum'])
        fielder_total_results.ops = f.on_base_plus_slugging(
            fielder_total_results.obp,
            fielder_total_results.slg)
        fielder_total_results.br = f.batting_runs(
            fielder_results['hit__sum'],
            fielder_results['two_base__sum'],
            fielder_results['three_base__sum'],
            fielder_results['home_run__sum'],
            fielder_results['bb_hbp__sum'],
            fielder_results['at_bat__sum']
        )
        fielder_total_results.woba = f.weighted_on_base_average(
            fielder_results['hit__sum'],
            fielder_results['two_base__sum'],
            fielder_results['three_base__sum'],
            fielder_results['home_run__sum'],
            fielder_results['bb_hbp__sum'],
            fielder_results['at_bat__sum']
        )
        fielder_total_results.gpa = f.gross_production_average(
            fielder_total_results.obp,
            fielder_total_results.slg)
        fielder_total_results.batting_average = f.batting_average(
            fielder_results['at_bat__sum'],
            fielder_results['hit__sum'])
        fielder_total_results.bbhp_percent = f.bb_hp_percentage(
            fielder_results['at_bat__sum'],
            fielder_results['bb_hbp__sum'],
            fielder_results['sacrifice_bunt__sum'])
        fielder_total_results.isod = f.isolated_discipline(
            fielder_total_results.obp,
            fielder_total_results.batting_average)
        fielder_total_results.isop = f.isolated_power(
            fielder_total_results.slg,
            fielder_total_results.batting_average)
        fielder_total_results.bbhp_k = f.bb_hbp_per_so(
            fielder_results['strike_out__sum'],
            fielder_results['bb_hbp__sum'])
        fielder_total_results.p_s = f.power_speed_number(
            fielder_results['home_run__sum'],
            fielder_results['stolen_base__sum'])

        return fielder_total_results

    def tally_from_player_all_results(self) -> FielderResults:
        """FielderResultsを集計する

        Returns:
            FielderResults: 対象選手の全てのFielderResultsを集計した結果を返す

        Notes:
            at_bat__sum, run__sum, hit__sum, two_base__sum, three_base__sum, home_run__sum,
            run_batted_in__sum, strike_out__sum, bb_hbp__sum, sacrifice_bunt__sum,
            stolen_base__sum, grounded_into_double_play__sum, error__sum
        """
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

    def tally_from_player_results_by_year(self) -> list:
        """選手詳細画面用に年度ごとにデータを集計する

        Returns:
            list: 年度ごとに以下を集計したList

        Notes:
            at_bat__sum, run__sum, hit__sum, two_base__sum, three_base__sum, home_run__sum,
            run_batted_in__sum, strike_out__sum, bb_hbp__sum, sacrifice_bunt__sum,
            stolen_base__sum, grounded_into_double_play__sum, error__sum
        """
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

    def tally_from_player_results_of_team(self) -> list:
        """チーム詳細画面用にデータを集計する

        Returns:
            list: 選手ごとに以下を集計したList

        Notes:
            at_bat__sum, run__sum, hit__sum, two_base__sum, three_base__sum, home_run__sum,
            run_batted_in__sum, strike_out__sum, bb_hbp__sum, sacrifice_bunt__sum,
            stolen_base__sum, grounded_into_double_play__sum, error__sum
        """
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

    def update_total_results(self, player_id: Players):
        """FielderTotalResultsを更新する

        Args:
            player_id (Players): 対象選手

        Returns:
            なし

        Notes:
            対象選手のFielderResultsを集計し、FielderTotalResultsを更新する
        """
        self.player_id = player_id
        fielder_results = self.tally_from_player_all_results()
        f = self.create_fielder_total_results(fielder_results)
        f.save()

    def update_all_total_results(self):
        """登録済みの全ての打者総合成績を更新する

        Args:
            なし

        Returns:
            なし
        """
        fielder_total_results = FielderTotalResults.objects.select_related(
            'player_id').all()
        update_fielder_results = []

        for ftr in fielder_total_results:
            self.player_id = ftr.player_id

            fielder_results = self.tally_from_player_all_results()
            # まだ試合に出ていない選手の場合はpassする
            if fielder_results["at_bat__sum"] is None:
                continue

            update_fielder_results.append(
                self.create_fielder_total_results(fielder_results))

        FielderTotalResults.objects.bulk_update(
            update_fielder_results,
            fields=[
                'at_bat',
                'run',
                'hit',
                'two_base',
                'three_base',
                'home_run',
                'run_batted_in',
                'strike_out',
                'bb_hbp',
                'sacrifice_bunt',
                'stolen_base',
                'grounded_into_double_play',
                'error',
                'total_bases',
                'slg',
                'obp',
                'ops',
                'br',
                'woba',
                'gpa',
                'batting_average',
                'bbhp_percent',
                'isod',
                'isop',
                'bbhp_k',
                'p_s'],
            batch_size=10000)
        print("打者総合成績を更新")

    def create_sabr_from_results_by_year(self, player_id: Players) -> list:
        """選手詳細画面用にデータを取得する

        Args:
            player_id (Players): 対象選手

        Returns:
            list: [{'year': year,'data': FielderTotalResults}]

        Notes:
            学年ごとに集計した打者成績を返す
        """
        self.player_id = player_id
        fielder_results = self.tally_from_player_results_by_year()
        fielder_total_results_list = []

        for result in fielder_results:
            f = self.create_fielder_total_results(result)
            fielder_total_results_list.append(
                {'year': result['game_id__team_id__year'], 'data': f})

        sorted_fielder_total_results_list = sorted(
            fielder_total_results_list, key=lambda x: x['year'], reverse=True)

        return sorted_fielder_total_results_list

    def create_sabr_from_results_of_team(self, team_id: Teams) -> list:
        """チーム詳細画面用にデータを取得する

        Args:
            team_id (Teams): 対象チーム

        Returns:
            list: [FielderTotalResults]

        Notes:
            対象チームの期間に所属している選手の、対象期間中の打者成績を返す
        """
        self.team_id = team_id
        fielder_results = self.tally_from_player_results_of_team()

        fielder_total_results_list = []

        for result in fielder_results:
            self.player_id = result['player_id']
            f = self.create_fielder_total_results(result)
            fielder_total_results_list.append(f)

        return fielder_total_results_list
