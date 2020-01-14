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
            error__sum=models.Sum('error'))

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
            home_run__sum=models.Sum('home_run'))

        pitcher_total_results_list = []
        for result in pitcher_results:
            pitcher_total_results = PitcherTotalResults.objects.select_related(
                'player_id').get(player_id=self.player_id)
            pitcher_total_results.games = result['games__count']
            pitcher_total_results.games_started = PitcherResults.objects.filter(
                player_id=self.player_id,
                game_id__team_id__year=result['game_id__team_id__year']).count()
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
        # Teamsのランクを更新する
        team = Teams.objects.latest('pk')
        team.runk = self.update_rank
        team.save()
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

        return team_total_results

    def update_results(self):
        t = self.create_sabr_from_results()
        t.save()
