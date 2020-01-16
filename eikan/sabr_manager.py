from django.db import models
from eikan.models import Teams, Games, \
    FielderResults, PitcherResults, \
    FielderTotalResults, PitcherTotalResults, \
    TeamTotalResults
from eikan.calculate_sabr import CalculateFielderSabr as f
from eikan.calculate_sabr import CalculatePitcherSabr as p
from eikan.calculate_sabr import CalculateTeamSabr as t


class FielderTotalSabrManager:
    def __init__(self, player_id):
        self.player_id = player_id

    def create_sabr_from_results(self):
        fielder_results = FielderResults.objects.filter(
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

        fielder_total_results = FielderTotalResults.objects.get(
            player_id=self.player_id)
        fielder_total_results.at_bat = fielder_results['at_bat__sum']
        fielder_total_results.run = fielder_results['run__sum']
        fielder_total_results.hit = fielder_results['hit__sum']
        fielder_total_results.two_base = fielder_results['two_base__sum']
        fielder_total_results.three_base = fielder_results['three_base__sum']
        fielder_total_results.home_run = fielder_results['home_run__sum']
        fielder_total_results.run_batted_in = fielder_results['run_batted_in__sum']
        fielder_total_results.strike_out = fielder_results['strike_out__sum']
        fielder_total_results.sacrifice_bunt = fielder_results['sacrifice_bunt__sum']
        fielder_total_results.stolen_base = fielder_results['stolen_base__sum']
        fielder_total_results.grounded_into_double_play = fielder_results[
            'grounded_into_double_play__sum']
        fielder_total_results.error = fielder_results['error__sum']
        fielder_total_results.total_bases = f.total_bases(
            self,
            fielder_results['hit__sum'],
            fielder_results['two_base__sum'],
            fielder_results['three_base__sum'],
            fielder_results['home_run__sum'])
        fielder_total_results.obp = f.on_base_percentage(
            self,
            fielder_results['at_bat__sum'],
            fielder_results['bb_hbp__sum'],
            fielder_results['hit__sum'])
        fielder_total_results.slg = f.slugging_percentage(
            self,
            fielder_results['at_bat__sum'],
            fielder_total_results.total_bases)
        fielder_total_results.ops = f.on_base_plus_slugging(
            self,
            fielder_total_results.obp,
            fielder_total_results.slg)
        fielder_total_results.br = f.batting_runs(
            self,
            fielder_results['hit__sum'],
            fielder_results['two_base__sum'],
            fielder_results['three_base__sum'],
            fielder_results['home_run__sum'],
            fielder_results['bb_hbp__sum'],
            fielder_results['at_bat__sum']
        )
        fielder_total_results.woba = f.weighted_on_base_average(
            self,
            fielder_results['hit__sum'],
            fielder_results['bb_hbp__sum'],
            fielder_results['at_bat__sum']
        )
        fielder_total_results.gpa = f.gross_production_average(
            self,
            fielder_total_results.obp,
            fielder_total_results.slg)
        fielder_total_results.batting_average = f.batting_average(
            self,
            fielder_results['at_bat__sum'],
            fielder_results['hit__sum'])
        fielder_total_results.bbhp_percent = f.bb_hp_percentage(
            self,
            fielder_results['at_bat__sum'],
            fielder_results['bb_hbp__sum'],
            fielder_results['sacrifice_bunt__sum'])
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
            fielder_results['strike_out__sum'],
            fielder_results['bb_hbp__sum'])
        fielder_total_results.p_s = f.power_speed_number(
            self,
            fielder_results['home_run__sum'],
            fielder_results['stolen_base__sum'])

        return fielder_total_results

    def update_results(self):
        f = self.create_sabr_from_results()
        f.save()


class PitcherTotalSabrManager:
    def __init__(self, player_id):
        self.player_id = player_id

    def create_sabr_from_results(self):
        pitcher_results = PitcherResults.objects.filter(
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

        sum_innings_pitched = (pitcher_results['innings_pitched__sum'] + (
            pitcher_results['innings_pitched_fraction__sum'] / 3)) * 3
        innings = float(
            pitcher_results['innings_pitched__sum'] +
            pitcher_results['innings_pitched_fraction__sum'] // 3)
        outcount = innings % 3
        if outcount == 1:
            innings += 0.1
        elif outcount == 2:
            innings += 0.2

        pitcher_total_results = PitcherTotalResults.objects.get(
            player_id=self.player_id)
        pitcher_total_results.games = PitcherResults.objects.filter(
            player_id=self.player_id).count()
        pitcher_total_results.games_started = PitcherResults.objects.filter(
            player_id=self.player_id, games_started=True).count()
        pitcher_total_results.innings_pitched = innings
        pitcher_total_results.number_of_pitch = pitcher_results['number_of_pitch__sum']
        pitcher_total_results.total_batters_faced = pitcher_results['total_batters_faced__sum']
        pitcher_total_results.hit = pitcher_results['hit__sum']
        pitcher_total_results.strike_out = pitcher_results['strike_out__sum']
        pitcher_total_results.bb_hbp = pitcher_results['bb_hbp__sum']
        pitcher_total_results.run = pitcher_results['run__sum']
        pitcher_total_results.earned_run = pitcher_results['earned_run__sum']
        pitcher_total_results.wild_pitch = pitcher_results['wild_pitch__sum']
        pitcher_total_results.home_run = pitcher_results['home_run__sum']
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
        self.team_score_difference = self.total_score['score__sum'] - \
            self.total_score['run__sum']
        self.team_batting_average = f.batting_average(
            self, self.fielder_results['at_bat__sum'],
            self.fielder_results['hit__sum'])
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
        # TeamTotalResultsを更新する
        team_total_results = TeamTotalResults.objects.get(team_id=self.team_id)
        team_total_results.total_win = self.total_win
        team_total_results.total_lose = self.total_lose
        team_total_results.total_draw = self.total_draw
        team_total_results.score = self.total_score['score__sum']
        team_total_results.run = self.total_score['run__sum']
        team_total_results.score_difference = self.team_score_difference
        team_total_results.batting_average = self.team_batting_average
        team_total_results.ops = self.team_ops
        team_total_results.hr = self.fielder_results['home_run__sum']
        team_total_results.era = self.team_era
        team_total_results.der = self.team_der

        if team_total_results.is_to_win:
            pass
        else:
            g = self.games.latest('pk')
            if g.competition_type > 3 and g.competiton_round == 8 and g.result == 1:
                team_total_results.is_to_win = True

        return team_total_results

    def update_results(self):
        # Teamsのランクを更新する
        team = Teams.objects.latest('pk')
        team.rank = self.update_rank
        team.save()
        # TeamsTotalResultsを更新する
        t = self.create_sabr_from_results()
        t.save()
