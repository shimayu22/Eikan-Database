from django.db import models
from eikan.models import Teams, Players, Games, Fielder_results, Pitcher_results

class CalculateSabr:
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

    def total_bases(self):
        # 安打 + 二塁打 + 三塁打 * 2 + 本塁打 * 3
        tb = self.total_hit + self.total_two_base + \
                      self.total_three_base * 2 + self.total_home_run * 3
        return tb
    
    def slugging_percentage(self, tb):
        # 塁打 / 打数
        slg = tb / self.total_at_bat
        return slg

    def on_base_percentage(self):
        # (安打数 + 四死球) / (打数 + 四死球)
        # 栄冠ナインの仕様上、犠飛を除外
        obp = (self.total_hit + self.total_bb_hbp) / \
              (self.total_at_bat + self.total_bb_hbp)
        return obp

    def on_base_plus_slugging(self, slg, obp):
        ops = slg + obp
        return ops

    def gross_production_average(self,slg, obp):
        gpa = (obp * 1.8 + obp) / 4
        return gpa
    
    def batting_average(self):
        ba = self.total_hit / self.total_at_bat
        return ba
    
    def bb_hbp_percentage(self):
        bbhp_per = self.total_bb_hbp / \
                    (self.total_at_bat + self.total_bb_hbp + self.total_sacrifice_bunt)
        return bbhp_per

    def isolated_discipline(self, obp, ba):
        isod = obp - ba
        return isod

    def isolated_power(self, slg, ba):
        isop = slg - ba
        return isop

    def bb_hbp_per_so(self):
        bbhp_so = self.total_bb_hbp / self.total_strike_out
        return bbhp_so
    
    def power_speed_number(self):
        p_s = (self.total_home_run * self.total_stolen_base * 2) / \
              (self.total_home_run + self.total_stolen_base)
        return p_s



