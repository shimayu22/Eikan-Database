"""打者成績に関する処理"""

from django.db import models

from eikan import sabr_calculations
from eikan.models import FielderResults, FielderTotalResults, Players, Teams


# bulk_updateで使用するフィールドリスト
FIELDER_TOTAL_RESULTS_UPDATE_FIELDS = [
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
    'p_s',
]


class FielderSabrFormatter:
    """主にFielderResults,FielderTotalResultsを操作する"""

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
            'player').get(player=self.player_id)
        
        # 集計結果を安全に取得（Noneの場合は0を返す）
        at_bat = fielder_results.get('at_bat__sum') or 0
        run = fielder_results.get('run__sum') or 0
        hit = fielder_results.get('hit__sum') or 0
        two_base = fielder_results.get('two_base__sum') or 0
        three_base = fielder_results.get('three_base__sum') or 0
        home_run = fielder_results.get('home_run__sum') or 0
        run_batted_in = fielder_results.get('run_batted_in__sum') or 0
        strike_out = fielder_results.get('strike_out__sum') or 0
        bb_hbp = fielder_results.get('bb_hbp__sum') or 0
        sacrifice_bunt = fielder_results.get('sacrifice_bunt__sum') or 0
        stolen_base = fielder_results.get('stolen_base__sum') or 0
        grounded_into_double_play = fielder_results.get('grounded_into_double_play__sum') or 0
        error = fielder_results.get('error__sum') or 0
        
        fielder_total_results.at_bat = at_bat
        fielder_total_results.run = run
        fielder_total_results.hit = hit
        fielder_total_results.two_base = two_base
        fielder_total_results.three_base = three_base
        fielder_total_results.home_run = home_run
        fielder_total_results.run_batted_in = run_batted_in
        fielder_total_results.strike_out = strike_out
        fielder_total_results.bb_hbp = bb_hbp
        fielder_total_results.sacrifice_bunt = sacrifice_bunt
        fielder_total_results.stolen_base = stolen_base
        fielder_total_results.grounded_into_double_play = grounded_into_double_play
        fielder_total_results.error = error
        
        fielder_total_results.total_bases = sabr_calculations.calculate_total_bases(
            hit, two_base, three_base, home_run)
        fielder_total_results.slg = sabr_calculations.calculate_slugging_percentage(
            at_bat, fielder_total_results.total_bases)
        fielder_total_results.obp = sabr_calculations.calculate_on_base_percentage(
            at_bat, bb_hbp, hit)
        fielder_total_results.ops = sabr_calculations.calculate_on_base_plus_slugging(
            fielder_total_results.obp, fielder_total_results.slg)
        fielder_total_results.br = sabr_calculations.calculate_batting_runs(
            hit, two_base, three_base, home_run, bb_hbp, at_bat)
        fielder_total_results.woba = sabr_calculations.calculate_weighted_on_base_average(
            hit, two_base, three_base, home_run, bb_hbp, at_bat)
        fielder_total_results.gpa = sabr_calculations.calculate_gross_production_average(
            fielder_total_results.obp, fielder_total_results.slg)
        fielder_total_results.batting_average = sabr_calculations.calculate_batting_average(
            at_bat, hit)
        fielder_total_results.bbhp_percent = sabr_calculations.calculate_bb_hp_percentage(
            at_bat, bb_hbp, sacrifice_bunt)
        fielder_total_results.isod = sabr_calculations.calculate_isolated_discipline(
            fielder_total_results.obp, fielder_total_results.batting_average)
        fielder_total_results.isop = sabr_calculations.calculate_isolated_power(
            fielder_total_results.slg, fielder_total_results.batting_average)
        fielder_total_results.bbhp_k = sabr_calculations.calculate_bb_hbp_per_so(
            strike_out, bb_hbp)
        fielder_total_results.p_s = sabr_calculations.calculate_power_speed_number(
            home_run, stolen_base)

        return fielder_total_results

    def tally_from_player_all_results(self) -> dict:
        """FielderResultsを集計する

        Returns:
            dict: 対象選手の全てのFielderResultsを集計した結果を返す

        Notes:
            at_bat__sum, run__sum, hit__sum, two_base__sum, three_base__sum, home_run__sum,
            run_batted_in__sum, strike_out__sum, bb_hbp__sum, sacrifice_bunt__sum,
            stolen_base__sum, grounded_into_double_play__sum, error__sum
        """
        fielder_results = FielderResults.objects.select_related('player').filter(
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

        Notes:
            再集計、再計算が行われる
        """
        fielder_total_results = FielderTotalResults.objects.select_related(
            'player').all()
        update_fielder_results = []

        for ftr in fielder_total_results:
            self.player_id = ftr.player

            fielder_results = self.tally_from_player_all_results()
            # まだ試合に出ていない選手の場合はpassする
            if fielder_results["at_bat__sum"] is None:
                continue

            update_fielder_results.append(
                self.create_fielder_total_results(fielder_results))

        if update_fielder_results:
            FielderTotalResults.objects.bulk_update(
                update_fielder_results,
                fields=FIELDER_TOTAL_RESULTS_UPDATE_FIELDS,
                batch_size=1000)

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
