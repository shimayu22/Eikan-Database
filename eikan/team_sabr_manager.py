"""チーム成績に関する処理"""

from django.db import models
from django.db.models import Max

from eikan import sabr_calculations
from eikan.model_manager import ChoicesFormatter as c
from eikan.models import (
    FielderResults,
    Games,
    PitcherResults,
    TeamTotalResults,
    Teams,
)

class TeamSabrFormatter:
    """チーム成績の集計、指標計算を行う"""

    def update_team_total_results(
            self,
            games_results: dict,
            fielder_results: dict,
            pitcher_results: dict,
            team_total_results: TeamTotalResults) -> TeamTotalResults:
        """集計したGames,FielderResults,PitcherResultsをもとに更新用のTeamTotalResultsを作る

        Args:
            games_results (dict): 集計したGames
            fielder_results (dict): 集計したFielderResults
            pitcher_results (dict): 集計したPitcherResults
            team_total_results (TeamTotalResults): 更新対象のTeamTotalResults

        Returns:
            TeamTotalResults: 計算した指標を代入したTeamTotalResults

        Notes:
            セイバーメトリクスはここで計算する
        """
        # 集計結果を安全に取得
        team_total_results.total_win = games_results.get('total_win', 0)
        team_total_results.total_lose = games_results.get('total_lose', 0)
        team_total_results.total_draw = games_results.get('total_draw', 0)
        team_total_results.score = games_results.get('score', 0)
        team_total_results.run = games_results.get('run', 0)
        team_total_results.score_difference = games_results.get('score_difference', 0)
        team_total_results.rank = games_results.get('update_rank', 0)
        team_total_results.cold_game = games_results.get('cold_game', 0)
        team_total_results.mamono_count = games_results.get('mamono_count', 0)
        team_total_results.mamono_score = games_results.get('mamono_score', 0)
        
        # 打者成績を安全に取得（Noneの場合は0を返す）
        f_at_bat = fielder_results.get('at_bat__sum') or 0
        f_hit = fielder_results.get('hit__sum') or 0
        f_two_base = fielder_results.get('two_base__sum') or 0
        f_three_base = fielder_results.get('three_base__sum') or 0
        f_home_run = fielder_results.get('home_run__sum') or 0
        f_bb_hbp = fielder_results.get('bb_hbp__sum') or 0
        f_error = fielder_results.get('error__sum') or 0
        
        team_total_results.hr = f_home_run

        team_total_results.batting_average = sabr_calculations.calculate_batting_average(
            f_at_bat, f_hit)
        team_obp = sabr_calculations.calculate_on_base_percentage(
            f_at_bat, f_bb_hbp, f_hit)
        team_tb = sabr_calculations.calculate_total_bases(
            f_hit, f_two_base, f_three_base, f_home_run)
        team_slg = sabr_calculations.calculate_slugging_percentage(f_at_bat, team_tb)
        team_total_results.ops = sabr_calculations.calculate_on_base_plus_slugging(
            team_obp, team_slg)
        team_total_results.br = sabr_calculations.calculate_batting_runs(
            f_hit, f_two_base, f_three_base, f_home_run, f_bb_hbp, f_at_bat)

        # 投手成績を安全に取得（Noneの場合は0を返す）
        p_innings_pitched = pitcher_results.get('innings_pitched__sum') or 0
        p_innings_pitched_fraction = pitcher_results.get('innings_pitched_fraction__sum') or 0
        p_earned_run = pitcher_results.get('earned_run__sum') or 0
        p_total_batters_faced = pitcher_results.get('total_batters_faced__sum') or 0
        p_hit = pitcher_results.get('hit__sum') or 0
        p_home_run = pitcher_results.get('home_run__sum') or 0
        p_bb_hbp = pitcher_results.get('bb_hbp__sum') or 0
        p_strike_out = pitcher_results.get('strike_out__sum') or 0
        
        total_sum_pi = (p_innings_pitched + (p_innings_pitched_fraction / 3)) * 3
        team_total_results.era = sabr_calculations.calculate_earned_runs_average(
            total_sum_pi, p_earned_run)
        team_total_results.der = sabr_calculations.calculate_team_der(
            p_total_batters_faced, p_hit, p_home_run, p_bb_hbp, p_strike_out, f_error)

        # 甲子園優勝したかチェックする
        competition_choices = c.competition_choices_to_dict()
        competition_round_choices = c.round_choices_to_dict()
        result_choices = c.result_choices_to_dict()

        # 一番勝ち進んだ試合を取得する
        competition_type_max = self.games.aggregate(
            Max('competition_type'))

        competition_round_max = self.games.filter(competition_type=competition_type_max['competition_type__max']).aggregate(
            Max('competition_round'))

        g = self.games.filter(
            competition_type=competition_type_max['competition_type__max'],
            competition_round=competition_round_max['competition_round__max']).latest('pk')

        # 優勝した判定
        team_total_results.is_to_win = g.competition_type > competition_choices[
            '地区大会'] and g.competition_round == competition_round_choices['決勝'] and g.result == result_choices['勝']

        # 一番勝ち進んだ戦績を登録する
        if team_total_results.is_to_win:
            game_record = game_record = Games.COMPETITION_CHOICES[
            competition_type_max['competition_type__max']][1] + "優勝"
        elif competition_type_max['competition_type__max'] == competition_choices['練習試合']:
            game_record = ""
        else:
            game_record = game_record = Games.COMPETITION_CHOICES[
            competition_type_max['competition_type__max']][1] + Games.ROUND_CHOICES[
                competition_round_max['competition_round__max']][1]
        team_total_results.game_record = game_record

        return team_total_results

    def tally_from_game_results(self) -> dict:
        """Gamesを集計する

        Returns:
            dict: 対象チームの全てのGamesを集計した結果を返す

        Notes:
            total_win, total_lose, total_draw, score, run,
            score_difference, update_rank, cold_game, mamono_count, mamono_score
        """
        games_results = {}
        games_results['total_win'] = self.games.filter(result=1).count()
        games_results['total_lose'] = self.games.filter(result=2).count()
        games_results['total_draw'] = self.games.filter(result=3).count()
        total_score = self.games.aggregate(
            models.Sum('score'), models.Sum('run'))
        games_results['score'] = total_score['score__sum']
        games_results['run'] = total_score['run__sum']
        games_results['score_difference'] = games_results['score'] - \
            games_results['run']
        games_results['update_rank'] = ["-", "弱小", "そこそこ",
                                        "中堅", "強豪", "名門"][self.games.latest('pk').rank]
        games_results['cold_game'] = self.games.filter(
            is_cold_game=True).count()
        games_results['mamono_count'] = self.games.aggregate(
            models.Sum('mamono_count'))['mamono_count__sum']
        games_results['mamono_score'] = self.games.aggregate(
            models.Sum('mamono_score'))['mamono_score__sum']

        return games_results

    def tally_from_fielder_results(self) -> dict:
        """FielderResultsを集計する

        Returns:
            dict: 対象選手の全てのFielderResultsを集計した結果を返す

        Notes:
            at_bat__sum, hit__sum, two_base__sum, three_base__sum,
            home_run__sum, bb_hbp__sum, error__sum
        """
        fielder_results = FielderResults.objects.select_related(
            'player_id', 'game_id').filter(game_id__in=self.games).aggregate(
                models.Sum('at_bat'),
                models.Sum('hit'),
                models.Sum('two_base'),
                models.Sum('three_base'),
                models.Sum('home_run'),
                models.Sum('bb_hbp'),
                models.Sum('error')
            )

        return fielder_results

    def tally_from_pitcher_results(self) -> dict:
        """PitcherResultsを集計する

        Returns:
            dict: 対象チームに所属する選手の全てのPitcherResultsを集計した結果を返す

        Notes:
            earned_run__sum, innings_pitched__sum, innings_pitched_fraction__sum,
            total_batters_faced__sum, hit__sum, bb_hbp__sum, strike_out__sum, home_run__sum
        """
        pitcher_results = PitcherResults.objects.select_related(
            'player_id', 'game_id').filter(game_id__in=self.games).aggregate(
                models.Sum('earned_run'),
                models.Sum('innings_pitched'),
                models.Sum('innings_pitched_fraction'),
                models.Sum('total_batters_faced'),
                models.Sum('hit'),
                models.Sum('bb_hbp'),
                models.Sum('strike_out'),
                models.Sum('home_run')
            )

        return pitcher_results

    def create_sabr_from_results_of_team(
            self, team_id: Teams) -> TeamTotalResults:
        """チーム詳細画面用にデータを取得する

        Args:
            team_id (Teams): 対象チーム

        Returns:
            TeamTotalResults: チーム総合成績を返す
        """
        self.team_id = team_id
        self.games = Games.objects.select_related(
            'team_id').filter(team_id=self.team_id)
        games_results = self.tally_from_game_results()
        fielder_results = self.tally_from_fielder_results()
        pitcher_results = self.tally_from_pitcher_results()
        team_total_results = self.update_team_total_results(
            games_results,
            fielder_results,
            pitcher_results,
            TeamTotalResults.objects.select_related('team').get(
                team=self.team_id))

        return team_total_results

    def update_total_results(self, team_id: Teams):
        """TeamsTotalResultsを更新する

        Args:
            team_id (Teams): 対象チーム

        Returns:
            なし

        Notes:
            対象チームのデータを集計、計算し更新する
            対象チームのGamesが未登録の場合は更新しない
        """
        if Games.objects.filter(team_id=team_id).exists():
            t = self.create_sabr_from_results_of_team(team_id)
            t.save()

    def update_all_total_results(self):
        """登録済みの全てのチーム総合成績を更新する

        Args:
            なし

        Returns:
            なし

        Notes:
            再集計、再計算が行われる
        """
        team_total_results = TeamTotalResults.objects.select_related(
            'team').all()
        update_team_results = []

        for ttr in team_total_results:
            if Games.objects.filter(team_id=ttr.team).exists():
                update_team_results.append(
                    self.create_sabr_from_results_of_team(
                        ttr.team))

        TeamTotalResults.objects.bulk_update(
            update_team_results,
            fields=[
                'total_win',
                'total_lose',
                'total_draw',
                'score',
                'run',
                'score_difference',
                'batting_average',
                'ops',
                'hr',
                'era',
                'der',
                'rank',
                'is_to_win',
                'game_record',
                'cold_game',
                'mamono_count',
                'mamono_score' ],
            batch_size=10000)
        print("チーム総合成績を更新")
