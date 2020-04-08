from django.db import models
from eikan.models import Games, \
    FielderResults, PitcherResults, \
    TeamTotalResults
from eikan.calculate_sabr import CalculateFielderSabr as f
from eikan.calculate_sabr import CalculatePitcherSabr as p
from eikan.calculate_sabr import CalculateTeamSabr as t


class TeamSabrFormatter:
    def __init__(self):
        self

    def update_team_total_results(
            self,
            games_results,
            fielder_results,
            pitcher_results,
            team_total_results):
        team_total_results.total_win = games_results['total_win']
        team_total_results.total_lose = games_results['total_lose']
        team_total_results.total_draw = games_results['total_draw']
        team_total_results.score = games_results['score']
        team_total_results.run = games_results['run']
        team_total_results.score_difference = games_results['score_difference']
        team_total_results.hr = fielder_results['home_run__sum']
        team_total_results.rank = games_results['update_rank']

        team_total_results.batting_average = f.batting_average(
            self,
            fielder_results['at_bat__sum'],
            fielder_results['hit__sum'])
        team_obp = f.on_base_percentage(
            self,
            fielder_results['at_bat__sum'],
            fielder_results['bb_hbp__sum'],
            fielder_results['hit__sum'])
        team_tb = f.total_bases(
            self,
            fielder_results['hit__sum'],
            fielder_results['two_base__sum'],
            fielder_results['three_base__sum'],
            fielder_results['home_run__sum'],)
        team_slg = f.slugging_percentage(
            self,
            fielder_results['at_bat__sum'], team_tb)
        team_total_results.ops = f.on_base_plus_slugging(
            self,
            team_obp, team_slg)

        total_sum_pi = (pitcher_results['innings_pitched__sum'] + (
            pitcher_results['innings_pitched_fraction__sum'] / 3)) * 3
        team_total_results.era = p.earned_runs_average(
            self,
            total_sum_pi,
            pitcher_results['earned_run__sum'])
        team_total_results.der = t.team_der(
            self,
            pitcher_results['total_batters_faced__sum'],
            pitcher_results['hit__sum'],
            pitcher_results['home_run__sum'],
            pitcher_results['bb_hbp__sum'],
            pitcher_results['strike_out__sum'],
            fielder_results['error__sum'])

        if team_total_results.is_to_win:
            pass
        else:
            g = self.games.latest('pk')
            if g.competition_type > 3 and g.competition_round == 8 and g.result == 1:
                team_total_results.is_to_win = True

        return team_total_results

    def tally_from_game_results(self):
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

        return games_results

    def tally_from_fielder_results(self):
        fielder_results = FielderResults.objects.select_related(
            'player_id', 'game_id').filter(game_id__in=self.games).aggregate(
            models.Sum('at_bat'),
            models.Sum('hit'),
            models.Sum('two_base'),
            models.Sum('three_base'),
            models.Sum('home_run'),
            models.Sum('bb_hbp'),
            models.Sum('error'))

        return fielder_results

    def tally_from_pitcher_results(self):
        pitcher_results = PitcherResults.objects.select_related(
            'player_id', 'game_id').filter(game_id__in=self.games).aggregate(
            models.Sum('earned_run'),
            models.Sum('innings_pitched'),
            models.Sum('innings_pitched_fraction'),
            models.Sum('total_batters_faced'),
            models.Sum('hit'),
            models.Sum('bb_hbp'),
            models.Sum('strike_out'),
            models.Sum('home_run'))

        return pitcher_results

    def create_sabr_from_results_of_team(self, team_id):
        # チーム詳細画面用にデータを取得するメソッド
        self.team_id = team_id
        self.games = Games.objects.select_related(
            'team_id').filter(team_id=self.team_id)
        games_results = self.tally_from_game_results()
        fielder_results = self.tally_from_fielder_results()
        pitcher_result = self.tally_from_pitcher_results()
        team_total_results = self.update_team_total_results(
            games_results,
            fielder_results,
            pitcher_result,
            TeamTotalResults.objects.select_related('team_id').get(
                team_id=self.team_id))

        return team_total_results

    def update_total_results(self, team_id):
        # TeamsTotalResults更新用メソッド
        if Games.objects.filter(team_id=team_id).exists():
            t = self.create_sabr_from_results_of_team(team_id)
            t.save()

    def update_all_total_results(self):
        # 登録済みの全てのチーム総合成績を更新する
        team_total_results = TeamTotalResults.objects.select_related(
            'team_id').all()
        update_team_results = []

        for ttr in team_total_results:
            if Games.objects.filter(team_id=ttr.team_id).exists():
                update_team_results.append(
                    self.create_sabr_from_results_of_team(
                        ttr.team_id))

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
                'is_to_win', ],
            batch_size=10000)
        print("チーム総合成績を更新")
