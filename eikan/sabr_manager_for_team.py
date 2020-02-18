from django.db import models
from eikan.models import FielderResults, PitcherResults, \
    FielderTotalResults, PitcherTotalResults
from eikan.calculate_sabr import CalculateFielderSabr as f
from eikan.calculate_sabr import CalculatePitcherSabr as p


class FielderByTeamSabrManager:
    def __init__(self, team_id):
        self.team_id = team_id

    def create_sabr_from_results(self):
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

        player_list = []
        for player in fielder_results:
            player_list.append(player['player_id'])

        fielder_total_results = FielderTotalResults.objects.select_related(
            'player_id').filter(player_id__in=player_list).order_by('player_id')

        for result, total_results in zip(
                fielder_results, fielder_total_results):
            total_results.at_bat = result['at_bat__sum']
            total_results.run = result['run__sum']
            total_results.hit = result['hit__sum']
            total_results.two_base = result['two_base__sum']
            total_results.three_base = result['three_base__sum']
            total_results.home_run = result['home_run__sum']
            total_results.run_batted_in = result['run_batted_in__sum']
            total_results.strike_out = result['strike_out__sum']
            total_results.bb_hbp = result['bb_hbp__sum']
            total_results.sacrifice_bunt = result['sacrifice_bunt__sum']
            total_results.stolen_base = result['stolen_base__sum']
            total_results.grounded_into_double_play = result[
                'grounded_into_double_play__sum']
            total_results.error = result['error__sum']
            total_results.total_bases = f.total_bases(
                self,
                result['hit__sum'],
                result['two_base__sum'],
                result['three_base__sum'],
                result['home_run__sum'])
            total_results.obp = f.on_base_percentage(
                self,
                result['at_bat__sum'],
                result['bb_hbp__sum'],
                result['hit__sum'])
            total_results.slg = f.slugging_percentage(
                self,
                result['at_bat__sum'],
                total_results.total_bases)
            total_results.ops = f.on_base_plus_slugging(
                self,
                total_results.obp,
                total_results.slg)
            total_results.br = f.batting_runs(
                self,
                result['hit__sum'],
                result['two_base__sum'],
                result['three_base__sum'],
                result['home_run__sum'],
                result['bb_hbp__sum'],
                result['at_bat__sum']
            )
            total_results.woba = f.weighted_on_base_average(
                self,
                result['hit__sum'],
                result['two_base__sum'],
                result['three_base__sum'],
                result['home_run__sum'],
                result['bb_hbp__sum'],
                result['at_bat__sum']
            )
            total_results.gpa = f.gross_production_average(
                self,
                total_results.obp,
                total_results.slg)
            total_results.batting_average = f.batting_average(
                self,
                result['at_bat__sum'],
                result['hit__sum'])
            total_results.bbhp_percent = f.bb_hp_percentage(
                self,
                result['at_bat__sum'],
                result['bb_hbp__sum'],
                result['sacrifice_bunt__sum'])
            total_results.isod = f.isolated_discipline(
                self,
                total_results.obp,
                total_results.batting_average)
            total_results.isop = f.isolated_power(
                self,
                total_results.slg,
                total_results.batting_average)
            total_results.bbhp_k = f.bb_hbp_per_so(
                self,
                result['strike_out__sum'],
                result['bb_hbp__sum'])
            total_results.p_s = f.power_speed_number(
                self,
                result['home_run__sum'],
                result['stolen_base__sum'])

        return fielder_total_results


class PitcherByTeamSabrManager:
    def __init__(self, team_id):
        self.team_id = team_id

    def create_sabr_from_results(self):
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

        player_list = []
        for player in pitcher_results:
            player_list.append(player['player_id'])

        pitcher_total_results = PitcherTotalResults.objects.select_related(
            'player_id').filter(player_id__in=player_list).order_by('player_id')

        for result, total_results in zip(
                pitcher_results, pitcher_total_results):
            total_results.games = result['games__count']
            total_results.games_started = PitcherResults.objects.filter(
                player_id=result['player_id'],
                game_id__team_id=self.team_id,
                games_started=True).count()
            sum_innings_pitched = p.innings_conversion_for_calculate(
                self, result['innings_pitched__sum'], result['innings_pitched_fraction__sum'])
            total_results.innings_pitched = p.innings_conversion_for_display(
                self, result['innings_pitched__sum'], result['innings_pitched_fraction__sum'])
            total_results.number_of_pitch = result['number_of_pitch__sum']
            total_results.total_batters_faced = result['total_batters_faced__sum']
            total_results.hit = result['hit__sum']
            total_results.strike_out = result['strike_out__sum']
            total_results.bb_hbp = result['bb_hbp__sum']
            total_results.run = result['run__sum']
            total_results.earned_run = result['earned_run__sum']
            total_results.wild_pitch = result['wild_pitch__sum']
            total_results.home_run = result['home_run__sum']
            total_results.era = p.earned_runs_average(
                self,
                sum_innings_pitched,
                result['earned_run__sum'])
            total_results.ura = p.runs_average(
                self,
                sum_innings_pitched,
                result['run__sum'])
            total_results.whip = p.walks_plus_hits_per_inning_pitched(
                self,
                sum_innings_pitched,
                result['hit__sum'],
                result['bb_hbp__sum'])
            total_results.k_bbhp = p.strike_out_per_bbhp(
                self,
                result['bb_hbp__sum'],
                result['strike_out__sum'])
            total_results.k_9 = p.strike_out_per_game(
                self,
                sum_innings_pitched,
                result['strike_out__sum'])
            total_results.k_percent = p.strike_out_percentage(
                self,
                result['total_batters_faced__sum'],
                result['strike_out__sum'])
            total_results.bbhp_9 = p.bbhp_per_game(
                self,
                sum_innings_pitched,
                result['bb_hbp__sum'])
            total_results.p_bbhp_percent = p.bbhp_percentage(
                self,
                result['total_batters_faced__sum'],
                result['bb_hbp__sum'])
            total_results.h_9 = p.hit_per_game(
                self,
                sum_innings_pitched,
                result['hit__sum']
            )
            total_results.h_percent = p.hit_percentage(
                self,
                result['total_batters_faced__sum'],
                result['hit__sum']
            )
            total_results.hr_9 = p.home_run_per_game(
                self,
                sum_innings_pitched,
                result['home_run__sum'])
            total_results.hr_percent = p.home_run_percentage(
                self,
                result['total_batters_faced__sum'],
                result['home_run__sum'])
            total_results.lob_percent = p.left_on_base_percentage(
                self,
                result['hit__sum'],
                result['bb_hbp__sum'],
                result['home_run__sum'],
                result['run__sum'])
            total_results.p_ip = p.pitch_per_inning(
                self,
                sum_innings_pitched,
                result['number_of_pitch__sum'])

        return pitcher_total_results
