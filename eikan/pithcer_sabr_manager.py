from django.db import models
from eikan.models import PitcherResults, PitcherTotalResults
from eikan.calculate_sabr import CalculatePitcherSabr as p


class PitcherSabrFormatter:
    def __init__(self):
        self

    def update_pitcher_total_results(
            self,
            pitcher_results,
            pitcher_total_results):
        sum_innings_pitched = p.innings_conversion_for_calculate(
            self,
            pitcher_results['innings_pitched__sum'],
            pitcher_results['innings_pitched_fraction__sum'])
        pitcher_total_results.games = PitcherResults.objects.filter(
            player_id=self.player_id).count()
        pitcher_total_results.games_started = PitcherResults.objects.filter(
            player_id=self.player_id, games_started=True).count()
        pitcher_total_results.number_of_pitch = pitcher_results['number_of_pitch__sum']
        pitcher_total_results.total_batters_faced = pitcher_results['total_batters_faced__sum']
        pitcher_total_results.hit = pitcher_results['hit__sum']
        pitcher_total_results.strike_out = pitcher_results['strike_out__sum']
        pitcher_total_results.bb_hbp = pitcher_results['bb_hbp__sum']
        pitcher_total_results.run = pitcher_results['run__sum']
        pitcher_total_results.earned_run = pitcher_results['earned_run__sum']
        pitcher_total_results.wild_pitch = pitcher_results['wild_pitch__sum']
        pitcher_total_results.home_run = pitcher_results['home_run__sum']
        pitcher_total_results.innings_pitched = p.innings_conversion_for_display(
            self,
            pitcher_results['innings_pitched__sum'],
            pitcher_results['innings_pitched_fraction__sum'])
        pitcher_total_results.era = p.earned_runs_average(
            self,
            sum_innings_pitched,
            pitcher_results['earned_run__sum'])
        pitcher_total_results.ura = p.runs_average(
            self,
            sum_innings_pitched,
            pitcher_results['run__sum'])
        pitcher_total_results.whip = p.walks_plus_hits_per_inning_pitched(
            self,
            sum_innings_pitched,
            pitcher_results['hit__sum'],
            pitcher_results['bb_hbp__sum'])
        pitcher_total_results.k_bbhp = p.strike_out_per_bbhp(
            self,
            pitcher_results['bb_hbp__sum'],
            pitcher_results['strike_out__sum'])
        pitcher_total_results.k_9 = p.strike_out_per_game(
            self,
            sum_innings_pitched,
            pitcher_results['strike_out__sum'])
        pitcher_total_results.k_percent = p.strike_out_percentage(
            self,
            pitcher_results['total_batters_faced__sum'],
            pitcher_results['strike_out__sum'])
        pitcher_total_results.bbhp_9 = p.bbhp_per_game(
            self,
            sum_innings_pitched,
            pitcher_results['bb_hbp__sum'])
        pitcher_total_results.p_bbhp_percent = p.bbhp_percentage(
            self,
            pitcher_results['total_batters_faced__sum'],
            pitcher_results['bb_hbp__sum'])
        pitcher_total_results.h_9 = p.hit_per_game(
            self,
            sum_innings_pitched,
            pitcher_results['hit__sum']
        )
        pitcher_total_results.h_percent = p.hit_percentage(
            self,
            pitcher_results['total_batters_faced__sum'],
            pitcher_results['hit__sum']
        )
        pitcher_total_results.hr_9 = p.home_run_per_game(
            self,
            sum_innings_pitched,
            pitcher_results['home_run__sum'])
        pitcher_total_results.hr_percent = p.home_run_percentage(
            self,
            pitcher_results['total_batters_faced__sum'],
            pitcher_results['home_run__sum'])
        pitcher_total_results.lob_percent = p.left_on_base_percentage(
            self,
            pitcher_results['hit__sum'],
            pitcher_results['bb_hbp__sum'],
            pitcher_results['home_run__sum'],
            pitcher_results['run__sum'])
        pitcher_total_results.p_ip = p.pitch_per_inning(
            self,
            sum_innings_pitched,
            pitcher_results['number_of_pitch__sum'])

        return pitcher_total_results

    def tally_from_player_all_results(self):
        pitcher_results = PitcherResults.objects.select_related('player_id').filter(
            player_id=self.player_id).aggregate(
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

        return pitcher_results
    
    def tally_from_player_results_by_year(self):
        pitcher_results = PitcherResults.objects.select_related(
            'game_id__team_id',
            'game_id',
            'player_id').filter(
            player_id=self.player_id).values(
            'game_id__team_id__year').annotate(
            games__count=models.Count('pk'),
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

        return pitcher_results

    def tally_from_player_results_of_team(self):
        pitcher_results = PitcherResults.objects.select_related(
            'game_id__team_id',
            'player_id').filter(
            game_id__team_id=self.team_id).values(
            'player_id').annotate(
            games__count=models.Count('pk'),
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

        return pitcher_results
        
    # PitcherTotalResults更新用メソッド
    def update_results(self, player_id):
        self.player_id = player_id
        pitcher_total_results = PitcherTotalResults.objects.select_related(
            'player_id').get(player_id=self.player_id)
        pitcher_results = self.tally_from_player_all_results()
        p = self.update_pitcher_total_results(pitcher_results, pitcher_total_results)
        p.save()

    # 投手詳細画面用にデータを取得するメソッド
    def create_sabr_from_results_by_year(self, player_id):
        self.player_id = player_id
        pitcher_total_results = PitcherTotalResults.objects.select_related(
            'player_id').get(player_id=self.player_id)
        pitcher_results = self.tally_from_player_results_by_year()
        pitcher_total_results_list = []

        for result in pitcher_results:
            p = self.update_fielder_total_results(
                result, pitcher_total_results)
            p.year = result['game_id__team_id__year']
            pitcher_total_results_list.append(p)

        return pitcher_total_results_list

    # チーム詳細画面用にデータを取得するメソッド
    def create_sabr_from_results_of_team(self, team_id):
        self.team_id = team_id
        pitcher_results = self.tally_from_player_results_of_team()
        player_list = []

        for player in pitcher_results:
            player_list.append(player['player_id'])

        pitcher_total_results = PitcherTotalResults.objects.select_related(
            'player_id').filter(player_id__in=player_list).order_by('player_id')
        pitcher_total_results_list = []

        for result, total_results in zip(
                pitcher_results, pitcher_total_results):
            p = self.update_fielder_total_results(
                result, total_results)
            pitcher_total_results_list.append(p)

        return pitcher_total_results_list
