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
        self.at_bat = fielder_results.aggregate(
            models.Sum('at_bat'))['at_bat__sum']
        self.run = fielder_results.aggregate(
            models.Sum('run'))['run__sum']
        self.hit = fielder_results.aggregate(
            models.Sum('hit'))['hit__sum']
        self.two_base = fielder_results.aggregate(
            models.Sum('two_base'))['two_base__sum']
        self.three_base = fielder_results.aggregate(
            models.Sum('three_base'))['three_base__sum']
        self.home_run = fielder_results.aggregate(
            models.Sum('home_run'))['home_run__sum']
        self.rbi = fielder_results.aggregate(
            models.Sum('run_batted_in'))['run_batted_in__sum']
        self.k = fielder_results.aggregate(
            models.Sum('strike_out'))['strike_out__sum']
        self.bb_hbp = fielder_results.aggregate(
            models.Sum('bb_hbp'))['bb_hbp__sum']
        self.sacrifice_bunt = fielder_results.aggregate(
            models.Sum('sacrifice_bunt'))['sacrifice_bunt__sum']
        self.strike_out = fielder_results.aggregate(
            models.Sum('strike_out'))['strike_out__sum']
        self.stolen_base = fielder_results.aggregate(
            models.Sum('stolen_base'))['stolen_base__sum']
        self.gibp = fielder_results.aggregate(
            models.Sum('grounded_into_double_play'))['grounded_into_double_play__sum']
        self.error = fielder_results.aggregate(
            models.Sum('error'))['error__sum']
        self.tb = f.total_bases(
            self,
            self.hit,
            self.two_base,
            self.three_base,
            self.home_run)
        self.obp = f.on_base_percentage(
            self, self.at_bat, self.bb_hbp, self.hit)
        self.slg = f.slugging_percentage(self, self.at_bat, self.tb)
        self.ops = f.on_base_plus_slugging(self, self.obp, self.slg)
        self.gpa = f.gross_production_average(self, self.obp, self.slg)
        self.ba = f.batting_average(self, self.at_bat, self.hit)
        self.bbhp_percent = f.bb_hp_percentage(
            self, self.at_bat, self.bb_hbp, self.sacrifice_bunt)
        self.isod = f.isolated_discipline(self, self.obp, self.ba)
        self.isop = f.isolated_power(self, self.slg, self.ba)
        self.bbhp_k = f.bb_hbp_per_so(self, self.strike_out, self.bb_hbp)
        self.p_s = f.power_speed_number(self, self.home_run, self.stolen_base)

    def create_sabr_from_results(self):
        fielder_total_results = FielderTotalResults.objects.get(
            player_id=self.player_id)
        fielder_total_results.at_bat = self.at_bat
        fielder_total_results.run = self.run
        fielder_total_results.hit = self.hit
        fielder_total_results.two_base = self.two_base
        fielder_total_results.three_base = self.three_base
        fielder_total_results.home_run = self.home_run
        fielder_total_results.run_batted_in = self.rbi
        fielder_total_results.strike_out = self.strike_out
        fielder_total_results.sacrifice_bunt = self.sacrifice_bunt
        fielder_total_results.stolen_base = self.stolen_base
        fielder_total_results.grounded_into_double_play = self.gibp
        fielder_total_results.error = self.error
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
        self.innings_pitched = pitcher_results.aggregate(
            models.Sum('innings_pitched'))['innings_pitched__sum']
        self.innings_pitched_fraction = pitcher_results.aggregate(
            models.Sum('innings_pitched_fraction'))['innings_pitched_fraction__sum']
        self.batters_faced = pitcher_results.aggregate(
            models.Sum('total_batters_faced'))['total_batters_faced__sum']
        self.number_of_pitch = pitcher_results.aggregate(
            models.Sum('number_of_pitch'))['number_of_pitch__sum']
        self.hit = pitcher_results.aggregate(
            models.Sum('hit'))['hit__sum']
        self.strike_out = pitcher_results.aggregate(
            models.Sum('strike_out'))['strike_out__sum']
        self.bb_hbp = pitcher_results.aggregate(
            models.Sum('bb_hbp'))['bb_hbp__sum']
        self.run = pitcher_results.aggregate(
            models.Sum('run'))['run__sum']
        self.earned_run = pitcher_results.aggregate(
            models.Sum('earned_run'))['earned_run__sum']
        self.wild_pitch = pitcher_results.aggregate(
            models.Sum('wild_pitch'))['wild_pitch__sum']
        self.home_run = pitcher_results.aggregate(
            models.Sum('home_run'))['home_run__sum']
        self.sum_innings_pitched = (
            self.innings_pitched + (self.innings_pitched_fraction / 3)) * 3
        self.innings = float(
            self.innings_pitched +
            self.innings_pitched_fraction //
            3)
        self.outcount = self.innings % 3
        if self.outcount == 1:
            self.innings += 0.1
        elif self.outcount == 2:
            self.innings += 0.2
        self.era = p.earned_runs_average(
            self, self.sum_innings_pitched, self.earned_run)
        self.ura = p.runs_average(self, self.sum_innings_pitched, self.run)
        self.whip = p.walks_plus_hits_per_inning_pitched(
            self, self.sum_innings_pitched, self.hit, self.bb_hbp)
        self.k_bbhp = p.strike_out_per_bbhp(self, self.bb_hbp, self.strike_out)
        self.k_9 = p.strike_out_per_game(
            self, self.sum_innings_pitched, self.strike_out)
        self.k_percent = p.strike_out_percentage(
            self, self.batters_faced, self.strike_out)
        self.bbhp_9 = p.bbhp_per_game(
            self, self.sum_innings_pitched, self.bb_hbp)
        self.p_bbhp_percent = p.bbhp_percentage(
            self, self.batters_faced, self.bb_hbp)
        self.hr_9 = p.home_run_per_game(
            self, self.sum_innings_pitched, self.home_run)
        self.hr_percent = p.home_run_percentage(
            self, self.batters_faced, self.home_run)
        self.lob_percent = p.left_on_base_percentage(
            self, self.hit, self.bb_hbp, self.home_run, self.run)
        self.p_ip = p.pitch_per_inning(
            self, self.sum_innings_pitched, self.number_of_pitch)

    def create_sabr_from_results(self):
        pitcher_total_results = PitcherTotalResults.objects.get(
            player_id=self.player_id)
        pitcher_total_results.games = self.game_count
        pitcher_total_results.games_started = self.games_started_count
        pitcher_total_results.innings_pitched = self.innings
        pitcher_total_results.number_of_pitch = self.number_of_pitch
        pitcher_total_results.total_batters_faced = self.batters_faced
        pitcher_total_results.hit = self.hit
        pitcher_total_results.strike_out = self.strike_out
        pitcher_total_results.bb_hbp = self.bb_hbp
        pitcher_total_results.run = self.run
        pitcher_total_results.earned_run = self.earned_run
        pitcher_total_results.wild_pitch = self.wild_pitch
        pitcher_total_results.home_run = self.home_run
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
        self.games = Games.objects.filter(team_id=self.team_id)
        self.total_win = self.games.filter(result=1).count()
        self.total_lose = self.games.filter(result=2).count()
        self.total_draw = self.games.filter(result=3).count()
        self.total_score = self.games.aggregate(
            models.Sum('score'))['score__sum']
        self.total_run = self.games.aggregate(models.Sum('run'))['run__sum']
        self.update_rank = ["-", "弱小", "そこそこ", "中堅",
                            "強豪", "名門"][self.games.latest('pk').rank]
        # Teams
        self.game = self.games.latest('pk')
        self.year = self.game.team_id.year
        self.period = self.game.team_id.period
        self.start_year = self.year - 2 if self.period == 1 else self.year - 1

        # FielderResults
        self.fielder_results = FielderResults.objects.filter(
            game_id__in=self.games)
        self.team_at_bat = self.fielder_results.aggregate(models.Sum('at_bat'))[
            'at_bat__sum']
        self.team_hit = self.fielder_results.aggregate(models.Sum('hit'))[
            'hit__sum']
        self.team_two_base = self.fielder_results.aggregate(
            models.Sum('two_base'))['two_base__sum']
        self.team_three_base = self.fielder_results.aggregate(
            models.Sum('three_base'))['three_base__sum']
        self.team_home_run = self.fielder_results.aggregate(
            models.Sum('home_run'))['home_run__sum']
        self.team_bbhp = self.fielder_results.aggregate(
            models.Sum('bb_hbp'))['bb_hbp__sum']
        self.team_error = self.fielder_results.aggregate(models.Sum('error'))[
            'error__sum']

        # PitcherResults
        self.pitcher_results = PitcherResults.objects.filter(
            game_id__in=self.games)
        self.team_er = self.pitcher_results.aggregate(
            models.Sum('earned_run'))['earned_run__sum']
        self.team_pi = self.pitcher_results.aggregate(
            models.Sum('innings_pitched'))['innings_pitched__sum']
        self.team_pi_fraction = self.pitcher_results.aggregate(
            models.Sum('innings_pitched_fraction'))['innings_pitched_fraction__sum']
        self.total_sum_pi = (self.team_pi + (self.team_pi_fraction / 3)) * 3
        self.team_total_batters_faced = self.pitcher_results.aggregate(
            models.Sum('total_batters_faced'))['total_batters_faced__sum']
        self.team_suffer_hit = self.pitcher_results.aggregate(models.Sum('hit'))[
            'hit__sum']
        self.team_bb_hbp = self.pitcher_results.aggregate(models.Sum('bb_hbp'))[
            'bb_hbp__sum']
        self.team_strike_out = self.pitcher_results.aggregate(
            models.Sum('strike_out'))['strike_out__sum']
        self.team_suffer_home_run = self.pitcher_results.aggregate(
            models.Sum('home_run'))['home_run__sum']
        self.team_score_difference = self.total_score - self.total_run
        self.team_batting_average = f.batting_average(
            self, self.team_at_bat, self.team_hit)
        self.team_obp = f.on_base_percentage(
            self, self.team_at_bat, self.team_bb_hbp, self.team_hit)
        self.team_tb = f.total_bases(
            self,
            self.team_hit,
            self.team_two_base,
            self.team_three_base,
            self.team_home_run)
        self.team_slg = f.slugging_percentage(
            self, self.team_at_bat, self.team_tb)
        self.team_ops = f.on_base_plus_slugging(
            self, self.team_obp, self.team_slg)
        self.team_era = p.earned_runs_average(
            self, self.total_sum_pi, self.team_er)
        self.team_der = t.team_der(
            self,
            self.team_total_batters_faced,
            self.team_suffer_hit,
            self.team_suffer_home_run,
            self.team_bb_hbp,
            self.team_strike_out,
            self.team_error)

    def create_sabr_from_results(self):
        # Teamsのランクを更新する
        self.game.team_id.rank = self.update_rank
        self.game.team_id.save()
        # TeamTotalResultsを更新する
        team_total_results = TeamTotalResults.objects.get(team_id=self.team_id)
        team_total_results.total_win = self.total_win
        team_total_results.total_lose = self.total_lose
        team_total_results.total_draw = self.total_draw
        team_total_results.score = self.total_score
        team_total_results.run = self.total_run
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
