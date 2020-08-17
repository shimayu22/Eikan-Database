"""投手成績に関する処理"""

from django.db import models
from eikan.models import PitcherResults, PitcherTotalResults, Players, Teams, Games
from eikan.calculate_sabr import CalculatePitcherSabr as p
from eikan.model_manager import ChoicesFormatter as c


class PitcherSabrFormatter:
    """主にPitcherResults,PitcherTotalResultsを操作する"""

    def __init__(self):
        self

    def create_pitcher_total_results(
            self,
            pitcher_results: PitcherResults) -> PitcherTotalResults:
        """集計したPitcherResultsをもとに更新用のPitcherTotalResultsを作る

        Args:
            pitcher_results (PitcherResults): 集計したPitcherResults

        Returns:
            PitcherTotalResults: 計算した指標を代入したPitcherTotalResults

        Notes:
            セイバーメトリクスはここで計算する
        """
        pitcher_total_results = PitcherTotalResults.objects.select_related(
            'player').get(player_id=self.player_id)
        pitcher_total_results.games = pitcher_results['pk__count']
        pitcher_total_results.games_started = pitcher_results['games_started']
        pitcher_total_results.number_of_pitch = pitcher_results['number_of_pitch__sum']
        pitcher_total_results.total_batters_faced = pitcher_results['total_batters_faced__sum']
        pitcher_total_results.hit = pitcher_results['hit__sum']
        pitcher_total_results.strike_out = pitcher_results['strike_out__sum']
        pitcher_total_results.bb_hbp = pitcher_results['bb_hbp__sum']
        pitcher_total_results.run = pitcher_results['run__sum']
        pitcher_total_results.earned_run = pitcher_results['earned_run__sum']
        pitcher_total_results.wild_pitch = pitcher_results['wild_pitch__sum']
        pitcher_total_results.home_run = pitcher_results['home_run__sum']
        pitcher_total_results.previous_game_pitched = pitcher_results['previous_game_pitched']

        sum_innings_pitched = p.innings_conversion_for_calculate(
            pitcher_results['innings_pitched__sum'],
            pitcher_results['innings_pitched_fraction__sum'])
        pitcher_total_results.innings_pitched = p.innings_conversion_for_display(
            pitcher_results['innings_pitched__sum'],
            pitcher_results['innings_pitched_fraction__sum'])
        pitcher_total_results.fip = p.fielding_independent_pitching(
            sum_innings_pitched,
            pitcher_results['home_run__sum'],
            pitcher_results['bb_hbp__sum'],
            pitcher_results['strike_out__sum'])
        pitcher_total_results.era = p.earned_runs_average(
            sum_innings_pitched,
            pitcher_results['earned_run__sum'])
        pitcher_total_results.ura = p.runs_average(
            sum_innings_pitched,
            pitcher_results['run__sum'])
        pitcher_total_results.whip = p.walks_plus_hits_per_inning_pitched(
            sum_innings_pitched,
            pitcher_results['hit__sum'],
            pitcher_results['bb_hbp__sum'])
        pitcher_total_results.k_bbhp = p.strike_out_per_bbhp(
            pitcher_results['bb_hbp__sum'],
            pitcher_results['strike_out__sum'])
        pitcher_total_results.k_9 = p.strike_out_per_game(
            sum_innings_pitched,
            pitcher_results['strike_out__sum'])
        pitcher_total_results.k_percent = p.strike_out_percentage(
            pitcher_results['total_batters_faced__sum'],
            pitcher_results['strike_out__sum'])
        pitcher_total_results.bbhp_9 = p.bbhp_per_game(
            sum_innings_pitched,
            pitcher_results['bb_hbp__sum'])
        pitcher_total_results.p_bbhp_percent = p.bbhp_percentage(
            pitcher_results['total_batters_faced__sum'],
            pitcher_results['bb_hbp__sum'])
        pitcher_total_results.h_9 = p.hit_per_game(
            sum_innings_pitched,
            pitcher_results['hit__sum']
        )
        pitcher_total_results.h_percent = p.hit_percentage(
            pitcher_results['total_batters_faced__sum'],
            pitcher_results['hit__sum']
        )
        pitcher_total_results.hr_9 = p.home_run_per_game(
            sum_innings_pitched,
            pitcher_results['home_run__sum'])
        pitcher_total_results.hr_percent = p.home_run_percentage(
            pitcher_results['total_batters_faced__sum'],
            pitcher_results['home_run__sum'])
        pitcher_total_results.lob_percent = p.left_on_base_percentage(
            pitcher_results['hit__sum'],
            pitcher_results['bb_hbp__sum'],
            pitcher_results['home_run__sum'],
            pitcher_results['run__sum'])
        pitcher_total_results.p_ip = p.pitch_per_inning(
            sum_innings_pitched,
            pitcher_results['number_of_pitch__sum'])

        return pitcher_total_results

    def create_previous_game_pitched(self) -> float:
        """1試合前に投げたイニングを取得する

        Returns:
            float: 1試合前に投げたイニングを返す ex)7.2

        Notes:
            練習試合、または登板していない場合は0を返す
        """
        competition_choices = c.competition_choices_to_dict()
        # GamesとPitcherResultsは必ず存在するのでチェックしない
        if Games.objects.latest(
                'pk').competition_type == competition_choices['練習試合']:
            return 0

        previous_game = Games.objects.filter(
            competition_type__gt=competition_choices['練習試合']).latest('pk')
        pr = PitcherResults.objects.select_related(
            'player_id', 'game_id').filter(
            game_id=previous_game, player_id=self.player_id)

        if pr.exists():
            pr_latest = pr.latest('pk')
            return p.innings_conversion_for_display(
                pr_latest.innings_pitched, pr_latest.innings_pitched_fraction)
        else:
            return 0

    def tally_from_player_all_results(self) -> dict:
        """PitcherResultsを集計する

        Returns:
            dict: 対象選手の全てのFielderResultsを集計した結果を返す

        Notes:
            pk__count, innings_pitched__sum, innings_pitched_fraction__sum,
            total_batters_faced__sum, total_batters_faced__sum,
            number_of_pitch__sum, hit__sum, strike_out__sum, bb_hbp__sum,
            run__sum, earned_run__sum, wild_pitch__sum, home_run__sum,
            games_started, previous_game_pitched
        """
        pitcher_results = PitcherResults.objects.select_related('player_id').filter(
            player_id=self.player_id).aggregate(
            models.Count('pk'),
            models.Sum('innings_pitched'),
            models.Sum('innings_pitched_fraction'),
            models.Sum('total_batters_faced'),
            models.Sum('number_of_pitch'),
            models.Sum('hit'),
            models.Sum('strike_out'),
            models.Sum('bb_hbp'),
            models.Sum('run'),
            models.Sum('earned_run'),
            models.Sum('wild_pitch'),
            models.Sum('home_run'))

        # PitcherResultsは必ず存在するのでチェックしない
        pitcher_results['games_started'] = PitcherResults.objects.select_related(
            'player_id').filter(player_id=self.player_id, games_started=True).count()

        # 前試合で投げたイニングを設定する
        pitcher_results['previous_game_pitched'] = self.create_previous_game_pitched()

        return pitcher_results

    def tally_from_player_results_by_year(self) -> list:
        """選手詳細画面用に年度ごとにデータを集計する

        Returns:
            list: 年度ごとに以下を集計したList

        Notes:
            pk__count, innings_pitched__sum, innings_pitched_fraction__sum,
            total_batters_faced__sum, total_batters_faced__sum,
            number_of_pitch__sum, hit__sum, strike_out__sum, bb_hbp__sum,
            run__sum, earned_run__sum, wild_pitch__sum, home_run__sum,
            games_started, previous_game_pitched
        """
        pitcher_results = PitcherResults.objects.select_related(
            'game_id__team_id',
            'game_id',
            'player_id').filter(
            player_id=self.player_id).values(
            'game_id__team_id__year').annotate(
            pk__count=models.Count('pk'),
            innings_pitched__sum=models.Sum('innings_pitched'),
            innings_pitched_fraction__sum=models.Sum('innings_pitched_fraction'),
            total_batters_faced__sum=models.Sum('total_batters_faced'),
            number_of_pitch__sum=models.Sum('number_of_pitch'),
            hit__sum=models.Sum('hit'),
            strike_out__sum=models.Sum('strike_out'),
            bb_hbp__sum=models.Sum('bb_hbp'),
            run__sum=models.Sum('run'),
            earned_run__sum=models.Sum('earned_run'),
            wild_pitch__sum=models.Sum('wild_pitch'),
            home_run__sum=models.Sum('home_run')).order_by('-game_id__team_id__year')

        for pi in pitcher_results:
            pi['games_started'] = PitcherResults.objects.filter(
                player_id=self.player_id,
                game_id__team_id__year=pi['game_id__team_id__year'],
                games_started=True).count()
            pi['previous_game_pitched'] = 0

        return pitcher_results

    def tally_from_player_results_of_team(self) -> list:
        """チーム詳細画面用にデータを集計する

        Returns:
            list: 選手ごとに以下を集計したList

        Notes:
            pk__count, innings_pitched__sum, innings_pitched_fraction__sum,
            total_batters_faced__sum, total_batters_faced__sum,
            number_of_pitch__sum, hit__sum, strike_out__sum, bb_hbp__sum,
            run__sum, earned_run__sum, wild_pitch__sum, home_run__sum,
            games_started, previous_game_pitched
        """
        pitcher_results = PitcherResults.objects.select_related(
            'game_id__team_id',
            'player_id').filter(
            game_id__team_id=self.team_id).values(
            'player_id').annotate(
            pk__count=models.Count('pk'),
            innings_pitched__sum=models.Sum('innings_pitched'),
            innings_pitched_fraction__sum=models.Sum(
                'innings_pitched_fraction'),
            total_batters_faced__sum=models.Sum('total_batters_faced'),
            number_of_pitch__sum=models.Sum('number_of_pitch'),
            hit__sum=models.Sum('hit'),
            strike_out__sum=models.Sum('strike_out'),
            bb_hbp__sum=models.Sum('bb_hbp'),
            run__sum=models.Sum('run'),
            earned_run__sum=models.Sum('earned_run'),
            wild_pitch__sum=models.Sum('wild_pitch'),
            home_run__sum=models.Sum('home_run')).order_by('player_id')

        for pi in pitcher_results:
            pi['games_started'] = PitcherResults.objects.select_related(
                'game_id__team_id',
                'player_id').filter(
                player_id=pi['player_id'],
                game_id__team_id=self.team_id,
                games_started=True).count()
            pi['previous_game_pitched'] = 0

        return pitcher_results

    def update_total_results(self, player_id: Players):
        """PitcherTotalResults更新用メソッド

        Args:
            player_id (Players): 対象選手

        Returns:
            なし

        Notes:
            対象選手のPitcherResultsを集計し、PitcherTotalResultsを更新する
        """
        self.player_id = player_id
        pitcher_results = self.tally_from_player_all_results()
        p = self.create_pitcher_total_results(pitcher_results)
        p.save()

    def update_all_total_results(self):
        """登録済みの全ての投手総合成績を更新する

        Args:
            なし

        Returns:
            なし

        Notes:
            再集計、再計算が行われる
        """
        pitcher_total_results = PitcherTotalResults.objects.select_related(
            'player').all()
        update_pitcher_results = []

        for ptr in pitcher_total_results:
            self.player_id = ptr.player

            pitcher_results = self.tally_from_player_all_results()
            # まだ試合に出ていない選手の場合はpassする
            if pitcher_results["innings_pitched__sum"] is None:
                continue

            update_pitcher_results.append(
                self.create_pitcher_total_results(pitcher_results))

        PitcherTotalResults.objects.bulk_update(
            update_pitcher_results,
            fields=[
                'games',
                'games_started',
                'innings_pitched',
                'number_of_pitch',
                'total_batters_faced',
                'hit',
                'strike_out',
                'bb_hbp',
                'run',
                'earned_run',
                'wild_pitch',
                'home_run',
                'fip',
                'era',
                'ura',
                'whip',
                'k_bbhp',
                'k_9',
                'k_percent',
                'bbhp_9',
                'p_bbhp_percent',
                'h_9',
                'h_percent',
                'hr_9',
                'hr_percent',
                'lob_percent',
                'p_ip',
                'previous_game_pitched'],
            batch_size=10000)
        print("投手総合成績を更新")

    def update_previous_game_pitched(self):
        """PitcherTotalResultsのprevious_game_pitchedを更新する

        Args:
            なし

        Returns:
            なし

        Notes:
            PitcherTotalResultsのprevious_game_pitchedのみを更新する
        """
        year = Teams.objects.latest('pk').year - 2
        pitchers = Players.objects.filter(
            is_pitcher=True, admission_year__gte=year)

        pitcher_total_results = PitcherTotalResults.objects.select_related(
            'player').filter(player_id__in=pitchers)
        for ptr in pitcher_total_results:
            self.player_id = ptr.player
            ptr.previous_game_pitched = self.create_previous_game_pitched()

        # 一括でUpdate(bulk_updateは通知がいかない)
        PitcherTotalResults.objects.bulk_update(
            pitcher_total_results, fields=["previous_game_pitched"])

    def create_sabr_from_results_by_year(self, player_id: Players) -> list:
        """選手詳細画面用にデータを取得する

        Args:
            player_id (Players): 対象選手

        Returns:
            list: [{'year': year, 'data': PitcherTotalResults}]
        """
        self.player_id = player_id
        pitcher_results = self.tally_from_player_results_by_year()
        pitcher_total_results_list = []

        for result in pitcher_results:
            p = self.create_pitcher_total_results(result)
            pitcher_total_results_list.append(
                {'year': result['game_id__team_id__year'], 'data': p})

        sorted_pitcher_total_results_list = sorted(
            pitcher_total_results_list, key=lambda x: x['year'], reverse=True)

        return sorted_pitcher_total_results_list

    def create_sabr_from_results_of_team(self, team_id: Teams) -> list:
        """チーム詳細画面用にデータを取得する

        Args:
            team_id (Teams): 対象チーム

        Returns:
            list: [PitcherTotalResults]
        """
        self.team_id = team_id
        pitcher_results = self.tally_from_player_results_of_team()

        pitcher_total_results_list = []

        for result in pitcher_results:
            self.player_id = result['player_id']
            p = self.create_pitcher_total_results(result)
            pitcher_total_results_list.append(p)

        return pitcher_total_results_list
