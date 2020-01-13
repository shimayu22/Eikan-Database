from django.db import models
from eikan.models import Games, \
    FielderResults, PitcherResults, \
    FielderTotalResults, PitcherTotalResults, \
    TeamTotalResults
from eikan.calculate_sabr import CalculateFielderSabr as f
from eikan.calculate_sabr import CalculatePitcherSabr as p
from eikan.calculate_sabr import CalculateTeamSabr as t


class FielderSabrManager:
    def __init__(self, player_id, fielder_results):
        self.player_id = player_id
        self.fielder_results = fielder_results.aggregate(
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
            models.Sum('strike_out'),
            models.Sum('stolen_base'),
            models.Sum('grounded_into_double_play'),
            models.Sum('error'))

        self.tb = f.total_bases(
            self,
            self.fielder_results['hit__sum'],
            self.fielder_results['two_base__sum'],
            self.fielder_results['three_base__sum'],
            self.fielder_results['home_run__sum'])
        self.obp = f.on_base_percentage(
            self,
            self.fielder_results['at_bat__sum'],
            self.fielder_results['bb_hbp__sum'],
            self.fielder_results['hit__sum'])
        self.slg = f.slugging_percentage(
            self, self.fielder_results['at_bat__sum'], self.tb)
        self.ops = f.on_base_plus_slugging(self, self.obp, self.slg)
        self.gpa = f.gross_production_average(self, self.obp, self.slg)
        self.ba = f.batting_average(self,
                                    self.fielder_results['at_bat__sum'],
                                    self.fielder_results['hit__sum'])
        self.bbhp_percent = f.bb_hp_percentage(
            self,
            self.fielder_results['at_bat__sum'],
            self.fielder_results['bb_hbp__sum'],
            self.fielder_results['sacrifice_bunt__sum'])
        self.isod = f.isolated_discipline(self, self.obp, self.ba)
        self.isop = f.isolated_power(self, self.slg, self.ba)
        self.bbhp_k = f.bb_hbp_per_so(self,
                                      self.fielder_results['strike_out__sum'],
                                      self.fielder_results['bb_hbp__sum'])
        self.p_s = f.power_speed_number(
            self,
            self.fielder_results['home_run__sum'],
            self.fielder_results['stolen_base__sum'])

    def create_sabr_from_results(self):
        fielder_total_results = FielderTotalResults.objects.get(
            player_id=self.player_id)
        fielder_total_results.at_bat = self.fielder_results['at_bat__sum']
        fielder_total_results.run = self.fielder_results['run__sum']
        fielder_total_results.hit = self.fielder_results['hit__sum']
        fielder_total_results.two_base = self.fielder_results['two_base__sum']
        fielder_total_results.three_base = self.fielder_results['three_base__sum']
        fielder_total_results.home_run = self.fielder_results['home_run__sum']
        fielder_total_results.run_batted_in = self.fielder_results['run_batted_in__sum']
        fielder_total_results.strike_out = self.fielder_results['strike_out__sum']
        fielder_total_results.sacrifice_bunt = self.fielder_results['sacrifice_bunt__sum']
        fielder_total_results.stolen_base = self.fielder_results['stolen_base__sum']
        fielder_total_results.grounded_into_double_play = self.fielder_results[
            'grounded_into_double_play__sum']
        fielder_total_results.error = self.fielder_results['error__sum']
        fielder_total_results.total_bases = self.tb
        fielder_total_results.obp = self.obp
        fielder_total_results.slg = self.slg
        fielder_total_results.ops = self.ops
        fielder_total_results.gpa = self.gpa
        fielder_total_results.batting_average = self.ba
        fielder_total_results.bbhp_percent = self.bbhp_percent
        fielder_total_results.isod = self.isod
        fielder_total_results.isop = self.isop
        fielder_total_results.bbhp_k = self.bbhp_k
        fielder_total_results.p_s = self.p_s

        return fielder_total_results

    def update_results(self):
        f = self.create_sabr_from_results()
        f.save()


class PitcherSabrManager:
    def __init__(self, player_id, pitcher_results):
        self.player_id = player_id
        self.game_count = pitcher_results.count()
        self.games_started_count = pitcher_results.filter(
            games_started=True).count()
        self.pitcher_results = pitcher_results.aggregate(
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

        self.sum_innings_pitched = (
            self.pitcher_results['innings_pitched__sum'] + (
                self.pitcher_results['innings_pitched_fraction__sum'] / 3)) * 3
        self.innings = float(
            self.pitcher_results['innings_pitched__sum'] +
            self.pitcher_results['innings_pitched_fraction__sum'] // 3)
        self.outcount = self.innings % 3
        if self.outcount == 1:
            self.innings += 0.1
        elif self.outcount == 2:
            self.innings += 0.2
        self.era = p.earned_runs_average(
            self,
            self.sum_innings_pitched,
            self.pitcher_results['earned_run__sum'])
        self.ura = p.runs_average(
            self,
            self.sum_innings_pitched,
            self.pitcher_results['run__sum'])
        self.whip = p.walks_plus_hits_per_inning_pitched(
            self,
            self.sum_innings_pitched,
            self.pitcher_results['hit__sum'],
            self.pitcher_results['bb_hbp__sum'])
        self.k_bbhp = p.strike_out_per_bbhp(
            self,
            self.pitcher_results['bb_hbp__sum'],
            self.pitcher_results['strike_out__sum'])
        self.k_9 = p.strike_out_per_game(
            self,
            self.sum_innings_pitched,
            self.pitcher_results['strike_out__sum'])
        self.k_percent = p.strike_out_percentage(
            self,
            self.pitcher_results['total_batters_faced__sum'],
            self.pitcher_results['strike_out__sum'])
        self.bbhp_9 = p.bbhp_per_game(
            self,
            self.sum_innings_pitched,
            self.pitcher_results['bb_hbp__sum'])
        self.p_bbhp_percent = p.bbhp_percentage(
            self,
            self.pitcher_results['total_batters_faced__sum'],
            self.pitcher_results['bb_hbp__sum'])
        self.hr_9 = p.home_run_per_game(
            self,
            self.sum_innings_pitched,
            self.pitcher_results['home_run__sum'])
        self.hr_percent = p.home_run_percentage(
            self,
            self.pitcher_results['total_batters_faced__sum'],
            self.pitcher_results['home_run__sum'])
        self.lob_percent = p.left_on_base_percentage(
            self,
            self.pitcher_results['hit__sum'],
            self.pitcher_results['bb_hbp__sum'],
            self.pitcher_results['home_run__sum'],
            self.pitcher_results['run__sum'])
        self.p_ip = p.pitch_per_inning(
            self,
            self.sum_innings_pitched,
            self.pitcher_results['number_of_pitch__sum'])

    def create_sabr_from_results(self):
        pitcher_total_results = PitcherTotalResults.objects.get(
            player_id=self.player_id)
        pitcher_total_results.games = self.game_count
        pitcher_total_results.games_started = self.games_started_count
        pitcher_total_results.innings_pitched = self.innings
        pitcher_total_results.number_of_pitch = self.pitcher_results['number_of_pitch__sum']
        pitcher_total_results.total_batters_faced = self.pitcher_results[
            'total_batters_faced__sum']
        pitcher_total_results.hit = self.pitcher_results['hit__sum']
        pitcher_total_results.strike_out = self.pitcher_results['strike_out__sum']
        pitcher_total_results.bb_hbp = self.pitcher_results['bb_hbp__sum']
        pitcher_total_results.run = self.pitcher_results['run__sum']
        pitcher_total_results.earned_run = self.pitcher_results['earned_run__sum']
        pitcher_total_results.wild_pitch = self.pitcher_results['wild_pitch__sum']
        pitcher_total_results.home_run = self.pitcher_results['home_run__sum']
        pitcher_total_results.era = self.era
        pitcher_total_results.ura = self.ura
        pitcher_total_results.whip = self.whip
        pitcher_total_results.k_bbhp = self.k_bbhp
        pitcher_total_results.k_9 = self.k_9
        pitcher_total_results.k_percent = self.k_percent
        pitcher_total_results.bbhp_9 = self.bbhp_9
        pitcher_total_results.p_bbhp_percent = self.p_bbhp_percent
        pitcher_total_results.hr_9 = self.hr_9
        pitcher_total_results.hr_percent = self.hr_percent
        pitcher_total_results.lob_percent = self.lob_percent
        pitcher_total_results.p_ip = self.p_ip

        return pitcher_total_results

    def update_results(self):
        p = self.create_sabr_from_results()
        p.save()


class TeamSabrManager:
    def __init__(self, team_id):
        self.team_id = team_id
        # Games
        self.games = Games.objects.select_related(
            'team_id').filter(team_id=self.team_id)
        self.total_win = self.games.filter(result=1).count()
        self.total_lose = self.games.filter(result=2).count()
        self.total_draw = self.games.filter(result=3).count()
        self.total_score = self.games.aggregate(
            models.Sum('score'), models.Sum('run'))
        self.update_rank = ["-", "弱小", "そこそこ", "中堅",
                            "強豪", "名門"][self.games.latest('pk').rank]
        # Teams
        self.year = self.games.team_id.latest('pk').year
        self.period = self.games.team_id.latest('pk').period
        self.start_year = self.year - 2 if self.period == 1 else self.year - 1

        # FielderResults
        self.fielder_results = FielderResults.objects.select_related(
            'player_id', 'game_id').filter(game_id__in=self.games).aggregate(
            models.Sum('at_bat'),
            models.Sum('hit'),
            models.Sum('two_base'),
            models.Sum('three_base'),
            models.Sum('home_run'),
            models.Sum('bb_hbp'),
            models.Sum('error'))

        # PitcherResults
        self.pitcher_results = PitcherResults.objects.select_related(
            'player_id', 'game_id').filter(game_id__in=self.games).aggregate(
            models.Sum('earned_run'),
            models.Sum('innings_pitched'),
            models.Sum('innings_pitched_fraction'),
            models.Sum('total_batters_faced'),
            models.Sum('hit'),
            models.Sum('bb_hbp'),
            models.Sum('strike_out'),
            models.Sum('home_run'))

        # チーム総合成績を算出する
        self.team_score_difference = self.total_score - self.total_run
        self.team_batting_average = f.batting_average(
            self, self.fielder_results['at_bat__sum'], self.fielder_results['hit__sum'])
        self.team_obp = f.on_base_percentage(
            self,
            self.fielder_results['at_bat__sum'],
            self.fielder_results['bb_hbp__sum'],
            self.fielder_results['hit__sum'])
        self.team_tb = f.total_bases(
            self,
            self.fielder_results['hit__sum'],
            self.fielder_results['two_base__sum'],
            self.fielder_results['three_base__sum'],
            self.fielder_results['home_run__sum'],)
        self.team_slg = f.slugging_percentage(
            self, self.fielder_results['at_bat__sum'], self.team_tb)
        self.team_ops = f.on_base_plus_slugging(
            self, self.team_obp, self.team_slg)
        self.total_sum_pi = (self.pitcher_results['innings_pitched__sum'] + (
            self.pitcher_results['innings_pitched_fraction__sum'] / 3)) * 3
        self.team_era = p.earned_runs_average(
            self, self.total_sum_pi, self.pitcher_results['earned_run__sum'])
        self.team_der = t.team_der(
            self,
            self.pitcher_results['total_batters_faced__sum'],
            self.pitcher_results['hit__sum'],
            self.pitcher_results['home_run__sum'],
            self.pitcher_results['bb_hbp__sum'],
            self.pitcher_results['strike_out__sum'],
            self.fielder_results['error__sum'])

    def create_sabr_from_results(self):
        # Teamsのランクを更新する
        self.game.team_id.rank = self.update_rank
        self.game.team_id.save()
        # TeamTotalResultsを更新する
        team_total_results = TeamTotalResults.objects.get(team_id=self.team_id)
        team_total_results.total_win = self.total_win
        team_total_results.total_lose = self.total_lose
        team_total_results.total_draw = self.total_draw
        team_total_results.score = self.total_score['score__sum']
        team_total_results.run = self.total_score['score__sum']
        team_total_results.score_difference = self.team_score_difference
        team_total_results.batting_average = self.team_batting_average
        team_total_results.ops = self.team_ops
        team_total_results.hr = self.team_home_run
        team_total_results.era = self.team_era
        team_total_results.der = self.team_der

        return team_total_results

    def update_results(self):
        t = self.create_sabr_from_results()
        t.save()
