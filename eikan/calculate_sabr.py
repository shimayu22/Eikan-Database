from django.db import models
from eikan.models import Teams, Players, Games, Fielder_results, Pitcher_results

class CalculateFielderSabr:
    def __init__(self, player_id):
        self.player_id = player_id
        self.fielder_results = Fielder_results.objects.filter(player_id=self.player_id)
        self.total_at_bat = self.fielder_results.aggregate(models.Sum('at_bat'))
        self.total_hit = self.fielder_results.aggregate(models.Sum('hit'))
        self.total_two_base = self.fielder_results.aggregate(models.Sum('two_base'))
        self.total_three_base = self.fielder_results.aggregate(models.Sum('three_base'))
        self.total_home_run = self.fielder_results.aggregate(models.Sum('home_run'))
        self.total_bb_hbp = self.fielder_results.aggregate(models.Sum('bb_hbp'))
        self.total_sacrifice_bunt = self.fielder_results.aggregate(models.Sum('sacrifice_bunt'))
        self.total_strike_out = self.fielder_results.aggregate(models.Sum('strike_out'))
        self.total_stolen_base = self.fielder_results.aggregate(models.Sum('stolen_base'))
        self.tb = 0
        self.slg = 0
        self.obp = 0
        self.ba = 0

    def total_bases(self):
        # 安打 + 二塁打 + 三塁打 * 2 + 本塁打 * 3
        tb = self.total_hit + self.total_two_base + \
                      self.total_three_base * 2 + self.total_home_run * 3
        self.tb = tb
        return self.tb
    
    def slugging_percentage(self):
        # 塁打 / 打数
        if self.total_at_bat == 0:
            return 0
        
        slg = self.tb / self.total_at_bat
        self.slg = slg
        return self.slg

    def on_base_percentage(self):
        # (安打数 + 四死球) / (打数 + 四死球)
        # 栄冠ナインの仕様上、犠飛を除外
        a = self.total_at_bat + self.total_bb_hbp
        if a == 0:
            return 0

        obp = (self.total_hit + self.total_bb_hbp) / a
        self.obp = obp
        return self.obp

    def on_base_plus_slugging(self):
        ops = self.slg + self.obp
        return ops

    def gross_production_average(self):
        gpa = (self.obp * 1.8 + self.obp) / 4
        return gpa
    
    def batting_average(self):
        if self.total_at_bat == 0:
            return 0

        ba = self.total_hit / self.total_at_bat
        self.ba = ba
        return self.ba
    
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


class CalculatePitcherSabr:
    def __init__(self, player_id):
        self.player_id = player_id
        self.pitcher_result = Pitcher_results.objects.filter(player_id=self.player_id)
        self.total_innings_pitched = self.pitcher_result.innings_pitched.aggregate(models.Sum('innings_pitched'))
        self.total_innings_pitched_fraction = self.pitcher_result.innings_pitched.aggregate(models.Sum('innings_pitched_fraction'))
        self.total_batters_faced = self.pitcher_result.innings_pitched.aggregate(models.Sum('total_batters_faced'))
        self.total_number_of_pitch = self.pitcher_result.innings_pitched.aggregate(models.Sum('number_of_pitch'))
        self.total_hit = self.pitcher_result.innings_pitched.aggregate(models.Sum('hit'))
        self.total_strike_out = self.pitcher_result.innings_pitched.aggregate(models.Sum('strike_out'))
        self.total_bb_hbp = self.pitcher_result.innings_pitched.aggregate(models.Sum('bb_hbp'))
        self.total_run = self.pitcher_result.innings_pitched.aggregate(models.Sum('run'))
        self.total_earned_run = self.pitcher_result.innings_pitched.aggregate(models.Sum('earned_run'))
        self.total_wild_pitch = self.pitcher_result.innings_pitched.aggregate(models.Sum('wild_pitch'))
        self.total_home_run = self.pitcher_result.innings_pitched.aggregate(models.Sum('home_run'))
        self.total_sum_innings_pitched = self.total_innings_pitched + self.total_innings_pitched_fraction

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

        whip = (self.total_hit + self.total_bb_hbp) / self.total_sum_innings_pitched
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

        k__percentage = self.total_strike_out / self.total_batters_faced
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
    
