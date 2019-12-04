from django.db import models
from eikan.models import Teams, Players, Games, \
                         FielderResults, PitcherResults, \
                         PlayersFielder, PlayersPitcher

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
        players_fielder = PlayersFielder.objects.get(player_id=self.player_id)
        players_fielder.at_bat = self.total_at_bat
        players_fielder.run = self.total_run
        players_fielder.hit = self.total_hit
        players_fielder.two_base = self.total_two_base
        players_fielder.three_base = self.total_three_base
        players_fielder.home_run = self.total_home_run
        players_fielder.run_batted_in = self.total_rbi
        players_fielder.strike_out = self.total_strike_out
        players_fielder.sacrifice_bunt = self.total_sacrifice_bunt
        players_fielder.stolen_base = self.total_stolen_base
        players_fielder.grounded_into_double_play = self.total_gibp
        players_fielder.error = self.total_error
        players_fielder.total_bases = self.total_bases()
        players_fielder.slg = self.slugging_percentage()
        players_fielder.obp = self.on_base_percentage()
        players_fielder.ops = self.on_base_plus_slugging()
        players_fielder.gpa = self.gross_production_average()
        players_fielder.batting_average = self.batting_average()
        players_fielder.bbhp_percent = self.bb_hp_percentage()
        players_fielder.isod = self.isolated_discipline()
        players_fielder.isop = self.isolated_power()
        players_fielder.bbhp_k = self.bb_hbp_per_so()
        players_fielder.p_s = self.power_speed_number()
        # 以上をupdateする
        players_fielder.save()


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
        players_pitcer = PlayersPitcher.objects.get(player_id=self.player_id)
        players_pitcer.games = self.game_count
        players_pitcer.games_started = self.games_started_count
        players_pitcer.innings_pitched = self.total_sum_innings_pitched
        players_pitcer.number_of_pitch = self.total_number_of_pitch
        players_pitcer.total_batters_faced = self.total_batters_faced
        players_pitcer.hit = self.total_hit
        players_pitcer.strike_out = self.total_strike_out
        players_pitcer.bb_hbp = self.total_bb_hbp
        players_pitcer.run = self.total_run
        players_pitcer.earned_run = self.total_earned_run
        players_pitcer.wild_pitch = self.total_wild_pitch
        players_pitcer.home_run = self.total_home_run
        players_pitcer.era = self.earned_runs_average()
        players_pitcer.ura = self.runs_average()
        players_pitcer.whip = self.walks_plus_hits_per_inning_pitched()
        players_pitcer.k_bbhp = self.strike_out_per_bbhp()
        players_pitcer.k_9 = self.strike_out_per_game()
        players_pitcer.k_percent = self.strike_out_percentage()
        players_pitcer.bbhp_9 = self.bbhp_per_game()
        players_pitcer.p_bbhp_percent = self.bbhp_percentage()
        players_pitcer.hr_9 = self.home_run_per_game()
        players_pitcer.hr_percent = self.home_run_percentage()
        players_pitcer.lob_percent = self.left_on_base_percentage()
        players_pitcer.p_ip = self.pitch_per_inning()
        # 上記をupdateする
        players_pitcer.save()
    
class CalculateTeamSabr:
    # TODO:うまい具合にチームの総計を取得して計算する
    def __init__(self, team_id):
        self.year = Teams.objects.filter(id=team_id).year
        self.period = Teams.objects.filter(id=team_id).period
        self.start_year = (self.year - 2) if self.period == 1 else (self.year - 1)
        self.players = Players.objects.filter(admission_year__gte=self.start_year, admission_year__lte=self.year)
        self.pitchers = Players.objects.filter(admission_year__gte=self.start_year, admission_year__lte=self.year, is_pitcher=True)

    def team_batting_average(self):
        self.players_at_bat = self.players.aggregate(models.Sum('at_bat'))['at_bat__sum']
        if self.players_at_bat == 0:
            return 0

        return self.players.aggregate(models.Sum('hit'))['hit__sum'] / self.players_at_bat
    
    def team_ops(self):
        return 0
        