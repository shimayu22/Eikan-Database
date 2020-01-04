from django.db import models

class CalculateFielderSabr:
    def total_bases(h,twobase,threebase,homurun):
        # 安打 + 二塁打 + 三塁打 * 2 + 本塁打 * 3
        return h + twobase + threebase * 2 + homerun * 3
    
    def slugging_percentage(at_bat, tb):
        # 塁打 / 打数
        if at_bat == 0:
            return 0
        
        return tb / at_bat

    def on_base_percentage(at_bat, bb_hbp, h):
        # (安打数 + 四死球) / (打数 + 四死球)
        # 栄冠ナインの仕様上、犠飛を除外
        a = at_bat + bb_hbp
        if a == 0:
            return 0

        return (h + bb_hbp) / a

    def on_base_plus_slugging(obp, slg):
        return obp + slg

    def gross_production_average(obp, slg):
        return (obp * 1.8 + slg) / 4
    
    def batting_average(at_bat, h):
        if at_bat == 0:
            return 0

        return h / at_bat
    
    def bb_hp_percentage(at_bat, bb_hbp, bunt):
        a = at_bat + bb_hbp + bunt
        if a == 0:
            return 0

        return bb_hbp / a

    def isolated_discipline(obp, ba):
        return obp - ba

    def isolated_power(slg, ba):
        return slg - ba

    def bb_hbp_per_so(strike_out, bb_hbp):
        if strike_out == 0:
            return 0

        return bb_hbp / strike_out
    
    def power_speed_number(home_run, stolen_base):
        a = home_run + stolen_base
        if a == 0:
            return 0

        return (shome_run * stolen_base * 2) / a

class CalculatePitcherSabr:
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
    
class CalculateTeamSabr:
    def team_der(self):
        a = self.team_total_batters_faced - self.team_suffer_hit - \
            self.team_bb_hbp - self.team_strike_out - self.team_error
        
        b = self.team_total_batters_faced - self.team_suffer_home_run - \
            self.team_bb_hbp - self.team_strike_out

        if b == 0:
            return 0

        return a / b
    
