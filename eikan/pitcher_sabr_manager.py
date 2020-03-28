from django.db import models
from eikan.models import PitcherResults, PitcherTotalResults, Players, Teams
from eikan.calculate_sabr import CalculatePitcherSabr as p


class PitcherSabrFormatter:
    def __init__(self):
        self

    def create_pitcher_total_results(
            self,
            pitcher_results):
        pitcher_total_results = PitcherTotalResults.objects.select_related(
            'player_id').get(player_id=self.player_id)
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
            self,
            pitcher_results['innings_pitched__sum'],
            pitcher_results['innings_pitched_fraction__sum'])
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

        pitcher_results['games_started'] = PitcherResults.objects.select_related(
            'player_id').filter(player_id=self.player_id, games_started=True).count()

        previous_game_pitcher_result = PitcherResults.objects.select_related(
            'player_id').filter(player_id=self.player_id).latest('pk').innings_pitched

        if previous_game_pitcher_result > 4:
            pitcher_results['previous_game_pitched'] = 1
        elif previous_game_pitcher_result > 2:
            pitcher_results['previous_game_pitched'] = 2
        elif previous_game_pitcher_result > 0:
            pitcher_results['previous_game_pitched'] = 3
        else:
            pitcher_results['previous_game_pitched'] = 0

        return pitcher_results

    def tally_from_player_results_by_year(self):
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

    def tally_from_player_results_of_team(self):
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

    def update_results(self, player_id):
        # PitcherTotalResults更新用メソッド
        self.player_id = player_id
        pitcher_results = self.tally_from_player_all_results()
        p = self.create_pitcher_total_results(pitcher_results)
        p.save()
    
    def update_previous_game_pitched(self):
        year = Teams.objects.latest('pk').year - 2
        pitchers = Players.objects.filter(is_pitcher=True, admission_year__gte=year)
        
        pitcher_total_results = PitcherTotalResults.objects.select_related('player_id').filter(player_id__in=pitchers)
        for ptr in pitcher_total_results:
            ptr.previous_game_pitched = 0
            ptr.save()

    def create_sabr_from_results_by_year(self, player_id):
        # 投手詳細画面用にデータを取得するメソッド
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

    def create_sabr_from_results_of_team(self, team_id):
        # チーム詳細画面用にデータを取得するメソッド
        self.team_id = team_id
        pitcher_results = self.tally_from_player_results_of_team()

        pitcher_total_results_list = []

        for result in pitcher_results:
            self.player_id = result['player_id']
            p = self.create_pitcher_total_results(result)
            pitcher_total_results_list.append(p)

        return pitcher_total_results_list
