from django.db import models
from eikan.models import Teams, Players, Games, \
                         FielderResults, PitcherResults, \
                         FielderTotalResults, PitcherTotalResults, \
                         TeamsTotalResults

class CalculateFielderSabr:
    def __init__(self, player_id):
        self.player_id = player_id
        self.fielder_results = FielderResults.objects.filter(player_id=self.player_id)
        self.total_at_bat = self.fielder_results.aggregate(models.Sum('at_bat'))['at_bat__sum']
        self.total_run = self.fielder_results.aggregate(models.Sum('run'))['run__sum']
        self.total_hit = self.fielder_results.aggregate(models.Sum('hit'))['hit__sum']
        self.total_two_base = self.fielder_results.aggregate(models.Sum('two_base'))['two_base__sum']
        self.total_three_base = self.fielder_results.aggregate(models.Sum('three_base'))['three_base__sum']
        self.total_home_run = self.fielder_results.aggregate(models.Sum('home_run'))['home_run__sum']
        self.total_rbi = self.fielder_results.aggregate(models.Sum('run_batted_in'))['run_batted_in__sum']
        self.total_k = self.fielder_results.aggregate(models.Sum('strike_out'))['strike_out__sum']
        self.total_bb_hbp = self.fielder_results.aggregate(models.Sum('bb_hbp'))['bb_hbp__sum']
        self.total_sacrifice_bunt = self.fielder_results.aggregate(models.Sum('sacrifice_bunt'))['sacrifice_bunt__sum']
        self.total_strike_out = self.fielder_results.aggregate(models.Sum('strike_out'))['strike_out__sum']
        self.total_stolen_base = self.fielder_results.aggregate(models.Sum('stolen_base'))['stolen_base__sum']
        self.total_gibp = self.fielder_results.aggregate(models.Sum('grounded_into_double_play'))['grounded_into_double_play__sum']
        self.total_error = self.fielder_results.aggregate(models.Sum('error'))['error__sum']
        self.tb = 0
        self.slg = 0
        self.obp = 0
        self.ba = 0

    def total_bases(self):
        # 安打 + 二塁打 + 三塁打 * 2 + 本塁打 * 3
        tb = self.total_hit + self.total_two_base + \
                      self.total_three_base * 2 + self.total_home_run * 3
        self.tb = tb
        return tb
    
    def slugging_percentage(self):
        # 塁打 / 打数
        if self.total_at_bat == 0:
            return 0
        
        slg = self.tb / self.total_at_bat
        self.slg = slg
        return slg

    def on_base_percentage(self):
        # (安打数 + 四死球) / (打数 + 四死球)
        # 栄冠ナインの仕様上、犠飛を除外
        a = self.total_at_bat + self.total_bb_hbp
        if a == 0:
            return 0

        obp = (self.total_hit + self.total_bb_hbp) / a
        self.obp = obp
        return obp

    def on_base_plus_slugging(self):
        ops = self.slg + self.obp
        return ops

    def gross_production_average(self):
        gpa = (self.obp * 1.8 + self.slg) / 4
        return gpa
    
    def batting_average(self):
        if self.total_at_bat == 0:
            return 0

        ba = self.total_hit / self.total_at_bat
        self.ba = ba
        return ba
    
    def bb_hp_percentage(self):
        a = self.total_at_bat + self.total_bb_hbp + self.total_sacrifice_bunt
        if a == 0:
            return 0

        bbhp_per = self.total_bb_hbp / a
        return bbhp_per

    def isolated_discipline(self):
        isod = self.obp - self.ba
        return isod

    def isolated_power(self):
        isop = self.slg - self.ba
        return isop

    def bb_hbp_per_so(self):
        if self.total_strike_out == 0:
            return 0

        bbhp_so = self.total_bb_hbp / self.total_strike_out
        return bbhp_so
    
    def power_speed_number(self):
        a = self.total_home_run + self.total_stolen_base
        if a == 0:
            return 0

        p_s = (self.total_home_run * self.total_stolen_base * 2) / a
        return p_s

    def update_total_results(self):
        fielder_total_results = FielderTotalResults.objects.get(player_id=self.player_id)
        fielder_total_results.at_bat = self.total_at_bat
        fielder_total_results.run = self.total_run
        fielder_total_results.hit = self.total_hit
        fielder_total_results.two_base = self.total_two_base
        fielder_total_results.three_base = self.total_three_base
        fielder_total_results.home_run = self.total_home_run
        fielder_total_results.run_batted_in = self.total_rbi
        fielder_total_results.strike_out = self.total_strike_out
        fielder_total_results.sacrifice_bunt = self.total_sacrifice_bunt
        fielder_total_results.stolen_base = self.total_stolen_base
        fielder_total_results.grounded_into_double_play = self.total_gibp
        fielder_total_results.error = self.total_error
        fielder_total_results.total_bases = self.total_bases()
        fielder_total_results.slg = self.slugging_percentage()
        fielder_total_results.obp = self.on_base_percentage()
        fielder_total_results.ops = self.on_base_plus_slugging()
        fielder_total_results.gpa = self.gross_production_average()
        fielder_total_results.batting_average = self.batting_average()
        fielder_total_results.bbhp_percent = self.bb_hp_percentage()
        fielder_total_results.isod = self.isolated_discipline()
        fielder_total_results.isop = self.isolated_power()
        fielder_total_results.bbhp_k = self.bb_hbp_per_so()
        fielder_total_results.p_s = self.power_speed_number()
        # 以上をupdateする
        fielder_total_results.save()


class CalculatePitcherSabr:
    def __init__(self, player_id):
        self.player_id = player_id
        self.pitcher_results = PitcherResults.objects.filter(player_id=self.player_id)
        self.game_count = self.pitcher_results.count()
        self.games_started_count = PitcherResults.objects.filter(player_id=self.player_id, games_started=True).count()
        self.total_innings_pitched = self.pitcher_results.aggregate(models.Sum('innings_pitched'))['innings_pitched__sum']
        self.total_innings_pitched_fraction = self.pitcher_results.aggregate(models.Sum('innings_pitched_fraction'))['innings_pitched_fraction__sum']
        self.total_batters_faced = self.pitcher_results.aggregate(models.Sum('total_batters_faced'))['total_batters_faced__sum']
        self.total_number_of_pitch = self.pitcher_results.aggregate(models.Sum('number_of_pitch'))['number_of_pitch__sum']
        self.total_hit = self.pitcher_results.aggregate(models.Sum('hit'))['hit__sum']
        self.total_strike_out = self.pitcher_results.aggregate(models.Sum('strike_out'))['strike_out__sum']
        self.total_bb_hbp = self.pitcher_results.aggregate(models.Sum('bb_hbp'))['bb_hbp__sum']
        self.total_run = self.pitcher_results.aggregate(models.Sum('run'))['run__sum']
        self.total_earned_run = self.pitcher_results.aggregate(models.Sum('earned_run'))['earned_run__sum']
        self.total_wild_pitch = self.pitcher_results.aggregate(models.Sum('wild_pitch'))['wild_pitch__sum']
        self.total_home_run = self.pitcher_results.aggregate(models.Sum('home_run'))['home_run__sum']
        self.total_sum_innings_pitched = (self.total_innings_pitched + (self.total_innings_pitched_fraction / 3)) * 3

    def earned_runs_average(self):
        if self.total_sum_innings_pitched == 0:
            return 0

        era = (self.total_earned_run * 9 * 3) / self.total_sum_innings_pitched
        return era

    def runs_average(self):
        if self.total_sum_innings_pitched == 0:
            return 0

        ra = (self.total_run * 9 * 3) / self.total_sum_innings_pitched
        return ra

    def walks_plus_hits_per_inning_pitched(self):
        if self.total_sum_innings_pitched == 0:
            return 0

        whip = (self.total_hit + self.total_bb_hbp) * 3 / self.total_sum_innings_pitched
        return whip

    def strike_out_per_bbhp(self):
        if self.total_bb_hbp == 0:
            return 0

        k_per_bbhp = self.total_strike_out / self.total_bb_hbp
        return k_per_bbhp
    
    def strike_out_per_game(self):
        if self.total_sum_innings_pitched == 0:
            return 0

        k_per_game = (self.total_strike_out * 9 * 3) / self.total_sum_innings_pitched
        return k_per_game
    
    def strike_out_percentage(self):
        if self.total_batters_faced == 0:
            return 0

        k_percentage = self.total_strike_out / self.total_batters_faced
        return k_percentage
    
    def bbhp_per_game(self):
        if self.total_sum_innings_pitched == 0:
            return 0

        bbhp_per_game = (self.total_bb_hbp * 9 * 3) / self.total_sum_innings_pitched
        return bbhp_per_game
    
    def bbhp_percentage(self):
        if self.total_batters_faced == 0:
            return 0
        
        bbhp_percentage = self.total_bb_hbp / self.total_batters_faced
        return bbhp_percentage
    
    def home_run_per_game(self):
        if self.total_sum_innings_pitched == 0:
            return 0

        hr_per_game = (self.total_home_run * 9 * 3) / self.total_sum_innings_pitched
        return hr_per_game
    
    def home_run_percentage(self):
        if self.total_batters_faced == 0:
            return 0
                
        hr_percentage = self.total_home_run / self.total_batters_faced
        return hr_percentage
    
    def left_on_base_percentage(self):
        a = self.total_hit + self.total_bb_hbp - self.total_home_run * 1.4
        if a == 0.0:
            return 0.0

        lob = (self.total_hit + self.total_bb_hbp - self.total_run) / a
        return lob
    
    def pitch_per_inning(self):
        if self.total_sum_innings_pitched == 0:
            return 0

        p_per_ip = (self.total_number_of_pitch * 3) / self.total_sum_innings_pitched
        return p_per_ip
    
    def update_total_results(self):
        pitcher_total_results = PitcherTotalResults.objects.get(player_id=self.player_id)
        pitcher_total_results.games = self.game_count
        pitcher_total_results.games_started = self.games_started_count
        innings = float(self.total_innings_pitched + self.total_innings_pitched_fraction // 3)
        outcount = self.total_innings_pitched_fraction % 3
        if outcount == 1:
            innings += 0.1
        elif outcount == 2:
            innings += 0.2
        pitcher_total_results.innings_pitched = innings
        pitcher_total_results.number_of_pitch = self.total_number_of_pitch
        pitcher_total_results.total_batters_faced = self.total_batters_faced
        pitcher_total_results.hit = self.total_hit
        pitcher_total_results.strike_out = self.total_strike_out
        pitcher_total_results.bb_hbp = self.total_bb_hbp
        pitcher_total_results.run = self.total_run
        pitcher_total_results.earned_run = self.total_earned_run
        pitcher_total_results.wild_pitch = self.total_wild_pitch
        pitcher_total_results.home_run = self.total_home_run
        pitcher_total_results.era = self.earned_runs_average()
        pitcher_total_results.ura = self.runs_average()
        pitcher_total_results.whip = self.walks_plus_hits_per_inning_pitched()
        pitcher_total_results.k_bbhp = self.strike_out_per_bbhp()
        pitcher_total_results.k_9 = self.strike_out_per_game()
        pitcher_total_results.k_percent = self.strike_out_percentage()
        pitcher_total_results.bbhp_9 = self.bbhp_per_game()
        pitcher_total_results.p_bbhp_percent = self.bbhp_percentage()
        pitcher_total_results.hr_9 = self.home_run_per_game()
        pitcher_total_results.hr_percent = self.home_run_percentage()
        pitcher_total_results.lob_percent = self.left_on_base_percentage()
        pitcher_total_results.p_ip = self.pitch_per_inning()
        # 上記をupdateする
        pitcher_total_results.save()
    
class CalculateTeamSabr:
    def __init__(self, team_id):
        # TeamsTotalResults
        self.teams_total_results = TeamsTotalResults.objects.get(team_id=team_id)
        self.year = self.teams_total_results.year
        self.period = self.teams_total_results.period
        self.start_year = (self.year - 2) if self.period == 1 else (self.year - 1)
        # Games
        self.games = Games.objects.filter(team_id=team_id)
        self.total_win = self.games.filter(result=1).count()
        self.total_lose = self.games.filter(result=2).count()
        self.total_draw = self.games.filter(result=3).count()
        self.total_score = self.games.aggregate(models.Sum('score'))['score__sum']
        self.total_run = self.games.aggregate(models.Sum('run'))['run__sum']
        self.latest_rank = self.games.latest('pk').rank
        # Players
        self.players = Players.objects.filter(admission_year__gte=self.start_year, admission_year__lte=self.year)
        self.pitchers = Players.objects.filter(admission_year__gte=self.start_year, admission_year__lte=self.year, is_pitcher=True)
        # FielderTotalResults
        self.fielder_total_results = FielderTotalResults.objects.filter(player_id__in=self.players)
        self.tema_at_bat = self.fielder_total_results.aggregate(models.Sum('at_bat'))['at_bat__sum']
        self.team_hit = self.fielder_total_results.aggregate(models.Sum('hit'))['hit__sum']
        self.team_two_base = self.fielder_total_results.aggregate(models.Sum('two_base'))['two_base__sum']
        self.team_three_base = self.fielder_total_results.aggregate(models.Sum('three_base'))['three_base__sum']
        self.team_home_run = self.fielder_total_results.aggregate(models.Sum('home_run'))['home_run__sum']
        self.team_bbhp = self.fielder_total_results.aggregate(models.Sum('bb_hbp'))['bb_hbp__sum']
        self.team_error = self.fielder_total_results.aggregate(models.Sum('error'))['error__sum']
        # PitcherTotalResults
        self.pitcher_total_results = PitcherTotalResults.objects.filter(player_id__in=self.pitchers)
        self.team_er = self.pitcher_total_results.aggregate(models.Sum('earned_run'))['earned_run__sum']
        self.team_pi = self.pitcher_total_results.aggregate(models.Sum('innings_pitched'))['innings_pitched__sum']
        self.team_total_batters_faced = self.pitcher_total_results.aggregate(models.Sum('total_batters_faced'))['total_batters_faced__sum']
        self.team_suffer_hit = self.pitcher_total_results.aggregate(models.Sum('hit'))['hit__sum']
        self.team_bb_hbp = self.pitcher_total_results.aggregate(models.Sum('bb_hbp'))['bb_hbp__sum']
        self.team_strike_out = self.pitcher_total_results.aggregate(models.Sum('strike_out'))['strike_out__sum']
        self.team_suffer_home_run = self.pitcher_total_results.aggregate(models.Sum('home_run'))['home_run__sum']


    def team_batting_average(self):
        if self.tema_at_bat == 0:
            return 0

        return self.team_hit / self.tema_at_bat
    
    def team_ops(self):
        if self.tema_at_bat == 0:
            return 0

        tb = self.team_hit + self.team_two_base + self.team_three_base * 2 + \
             self.team_home_run * 3
        slg = tb / self.tema_at_bat
        obp = (self.team_hit + self.team_bbhp) / (self.tema_at_bat + self.team_bbhp)

        return slg + obp
    
    def team_era(self):
        ip = int(self.team_pi)
        outcount = 0
        if self.team_pi - ip == 0.1:
            outcount = 1
        elif self.team_pi - ip == 0.2:
            outcount = 2

        if self.team_pi < 0.1:
            return 0
        
        return (self.team_er * 9 * 3) / ((ip + (outcount / 3)) * 3)
    
    def team_der(self):
        a = self.team_total_batters_faced - self.team_suffer_hit - \
            self.team_bb_hbp - self.team_strike_out - self.team_error
        
        b = self.team_total_batters_faced - self.team_suffer_home_run - \
            self.team_bb_hbp - self.team_strike_out

        if b == 0:
            return 0

        return a / b
    
    def update_total_results(self):
        self.teams_total_results.total_win = self.total_win
        self.teams_total_results.total_lose = self.total_lose
        self.teams_total_results.total_draw = self.total_draw
        self.teams_total_results.score = self.total_score
        self.teams_total_results.run = self.total_run
        self.teams_total_results.score_difference = self.total_score - self.total_run
        self.teams_total_results.rank = self.latest_rank
        self.teams_total_results.batting_average = self.team_batting_average()
        self.teams_total_results.ops = self.team_ops()
        self.teams_total_results.hr = self.home_run
        self.teams_total_results.era = self.team_era()
        self.teams_total_results.der = self.team_der()
        # 以上をupdateする
        self.teams_total_results.save()