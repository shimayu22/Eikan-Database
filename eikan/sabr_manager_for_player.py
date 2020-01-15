from django.db import models
from eikan.models import Teams, Games, \
    FielderResults, PitcherResults, \
    FielderTotalResults, PitcherTotalResults
from eikan.calculate_sabr import CalculateFielderSabr as f
from eikan.calculate_sabr import CalculatePitcherSabr as p


class FielderByYearSabrManager:
    def __init__(self, player_id):
        self.player_id = player_id

    def create_sabr_from_results(self):
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
            grounded_into_double_play__sum=models.Sum('grounded_into_double_play'),
            error__sum=models.Sum('error')).order_by('-game_id__team_id__year')

        fielder_total_results_list = []

        for result in fielder_results:
            fielder_total_results = FielderTotalResults.objects.select_related(
                'player_id').get(player_id=self.player_id)
            fielder_total_results.at_bat = result['at_bat__sum']
            fielder_total_results.run = result['run__sum']
            fielder_total_results.hit = result['hit__sum']
            fielder_total_results.two_base = result['two_base__sum']
            fielder_total_results.three_base = result['three_base__sum']
            fielder_total_results.home_run = result['home_run__sum']
            fielder_total_results.run_batted_in = result['run_batted_in__sum']
            fielder_total_results.strike_out = result['strike_out__sum']
            fielder_total_results.sacrifice_bunt = result['sacrifice_bunt__sum']
            fielder_total_results.stolen_base = result['stolen_base__sum']
            fielder_total_results.grounded_into_double_play = result[
                'grounded_into_double_play__sum']
            fielder_total_results.error = result['error__sum']
            fielder_total_results.total_bases = f.total_bases(
                self,
                result['hit__sum'],
                result['two_base__sum'],
                result['three_base__sum'],
                result['home_run__sum'])
            fielder_total_results.obp = f.on_base_percentage(
                self,
                result['at_bat__sum'],
                result['bb_hbp__sum'],
                result['hit__sum'])
            fielder_total_results.slg = f.slugging_percentage(
                self,
                result['at_bat__sum'],
                fielder_total_results.total_bases)
            fielder_total_results.ops = f.on_base_plus_slugging(
                self,
                fielder_total_results.obp,
                fielder_total_results.slg)
            fielder_total_results.gpa = f.gross_production_average(
                self,
                fielder_total_results.obp,
                fielder_total_results.slg)
            fielder_total_results.batting_average = f.batting_average(
                self,
                result['at_bat__sum'],
                result['hit__sum'])
            fielder_total_results.bbhp_percent = f.bb_hp_percentage(
                self,
                result['at_bat__sum'],
                result['bb_hbp__sum'],
                result['sacrifice_bunt__sum'])
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
                result['strike_out__sum'],
                result['bb_hbp__sum'])
            fielder_total_results.p_s = f.power_speed_number(
                self,
                result['home_run__sum'],
                result['stolen_base__sum'])
            fielder_total_results_list.append(
                [result['game_id__team_id__year'], fielder_total_results])

        return fielder_total_results_list


class PitcherByYearSabrManager:
    def __init__(self, player_id):
        self.player_id = player_id

    def create_sabr_from_results(self):
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

        pitcher_total_results_list = []
        for result in pitcher_results:
            pitcher_total_results = PitcherTotalResults.objects.select_related(
                'player_id').get(player_id=self.player_id)
            pitcher_total_results.games = result['games__count']
            pitcher_total_results.games_started = PitcherResults.objects.filter(
                player_id=self.player_id,
                game_id__team_id__year=result['game_id__team_id__year'],
                games_started=True).count()
            sum_innings_pitched = (
                result['innings_pitched__sum'] + (result['innings_pitched_fraction__sum'] / 3)) * 3
            innings = float(result['innings_pitched__sum'] +
                            result['innings_pitched_fraction__sum'] // 3)
            outcount = innings % 3
            if outcount == 1:
                innings += 0.1
            elif outcount == 2:
                innings += 0.2
            pitcher_total_results.innings_pitched = innings
            pitcher_total_results.number_of_pitch = result['number_of_pitch__sum']
            pitcher_total_results.total_batters_faced = result['total_batters_faced__sum']
            pitcher_total_results.hit = result['hit__sum']
            pitcher_total_results.strike_out = result['strike_out__sum']
            pitcher_total_results.bb_hbp = result['bb_hbp__sum']
            pitcher_total_results.run = result['run__sum']
            pitcher_total_results.earned_run = result['earned_run__sum']
            pitcher_total_results.wild_pitch = result['wild_pitch__sum']
            pitcher_total_results.home_run = result['home_run__sum']
            pitcher_total_results.era = p.earned_runs_average(
                self,
                sum_innings_pitched,
                result['earned_run__sum'])
            pitcher_total_results.ura = p.runs_average(
                self,
                sum_innings_pitched,
                result['run__sum'])
            pitcher_total_results.whip = p.walks_plus_hits_per_inning_pitched(
                self,
                sum_innings_pitched,
                result['hit__sum'],
                result['bb_hbp__sum'])
            pitcher_total_results.k_bbhp = p.strike_out_per_bbhp(
                self,
                result['bb_hbp__sum'],
                result['strike_out__sum'])
            pitcher_total_results.k_9 = p.strike_out_per_game(
                self,
                sum_innings_pitched,
                result['strike_out__sum'])
            pitcher_total_results.k_percent = p.strike_out_percentage(
                self,
                result['total_batters_faced__sum'],
                result['strike_out__sum'])
            pitcher_total_results.bbhp_9 = p.bbhp_per_game(
                self,
                sum_innings_pitched,
                result['bb_hbp__sum'])
            pitcher_total_results.p_bbhp_percent = p.bbhp_percentage(
                self,
                result['total_batters_faced__sum'],
                result['bb_hbp__sum'])
            pitcher_total_results.hr_9 = p.home_run_per_game(
                self,
                sum_innings_pitched,
                result['home_run__sum'])
            pitcher_total_results.hr_percent = p.home_run_percentage(
                self,
                result['total_batters_faced__sum'],
                result['home_run__sum'])
            pitcher_total_results.lob_percent = p.left_on_base_percentage(
                self,
                result['hit__sum'],
                result['bb_hbp__sum'],
                result['home_run__sum'],
                result['run__sum'])
            pitcher_total_results.p_ip = p.pitch_per_inning(
                self,
                sum_innings_pitched,
                result['number_of_pitch__sum'])

            pitcher_total_results_list.append(
                [result['game_id__team_id__year'], pitcher_total_results])

        return pitcher_total_results_list
