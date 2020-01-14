class CalculateFielderSabr:
    def total_bases(self, h, twobase, threebase, homerun):
        # 安打 + 二塁打 + 三塁打 * 2 + 本塁打 * 3
        return h + twobase + threebase * 2 + homerun * 3

    def slugging_percentage(self, at_bat, tb):
        # 塁打 / 打数
        if at_bat == 0:
            return 0

        return tb / at_bat

    def on_base_percentage(self, at_bat, bb_hbp, h):
        # (安打数 + 四死球) / (打数 + 四死球)
        # 栄冠ナインの仕様上、犠飛を除外
        a = at_bat + bb_hbp
        if a == 0:
            return 0

        return (h + bb_hbp) / a

    def on_base_plus_slugging(self, obp, slg):
        return obp + slg

    def gross_production_average(self, obp, slg):
        return (obp * 1.8 + slg) / 4

    def batting_average(self, at_bat, h):
        if at_bat == 0:
            return 0

        return h / at_bat

    def bb_hp_percentage(self, at_bat, bb_hbp, bunt):
        a = at_bat + bb_hbp + bunt
        if a == 0:
            return 0

        return bb_hbp / a

    def isolated_discipline(self, obp, ba):
        return obp - ba

    def isolated_power(self, slg, ba):
        return slg - ba

    def bb_hbp_per_so(self, strike_out, bb_hbp):
        if strike_out == 0:
            return 0

        return bb_hbp / strike_out

    def power_speed_number(self, home_run, stolen_base):
        a = home_run + stolen_base
        if a == 0:
            return 0

        return (home_run * stolen_base * 2) / a


class CalculatePitcherSabr:
    def earned_runs_average(self, sum_innings_pitched, earned_run):
        if sum_innings_pitched == 0:
            return 0

        return (earned_run * 9 * 3) / sum_innings_pitched

    def runs_average(self, sum_innings_pitched, run):
        if sum_innings_pitched == 0:
            return 0

        return (run * 9 * 3) / sum_innings_pitched

    def walks_plus_hits_per_inning_pitched(
            self, sum_innings_pitched, hit, bb_hbp):
        if sum_innings_pitched == 0:
            return 0

        return (hit + bb_hbp) * 3 / sum_innings_pitched

    def strike_out_per_bbhp(self, bb_hbp, strike_out):
        if bb_hbp == 0:
            return 0

        return strike_out / bb_hbp

    def strike_out_per_game(self, sum_innings_pitched, strike_out):
        if sum_innings_pitched == 0:
            return 0

        return (strike_out * 9 * 3) / sum_innings_pitched

    def strike_out_percentage(self, batters_faced, strike_out):
        if batters_faced == 0:
            return 0

        return strike_out / batters_faced

    def bbhp_per_game(self, sum_innings_pitched, bb_hbp):
        if sum_innings_pitched == 0:
            return 0

        return (bb_hbp * 9 * 3) / sum_innings_pitched

    def bbhp_percentage(self, batters_faced, bb_hbp):
        if batters_faced == 0:
            return 0

        return bb_hbp / batters_faced

    def home_run_per_game(self, sum_innings_pitched, home_run):
        if sum_innings_pitched == 0:
            return 0

        return (home_run * 9 * 3) / sum_innings_pitched

    def home_run_percentage(self, batters_faced, home_run):
        if batters_faced == 0:
            return 0

        return home_run / batters_faced

    def left_on_base_percentage(self, hit, bb_hbp, home_run, run):
        a = hit + bb_hbp - home_run * 1.4
        if a == 0.0:
            return 0.0

        return (hit + bb_hbp - run) / a

    def pitch_per_inning(self, sum_innings_pitched, number_of_pitch):
        if sum_innings_pitched == 0:
            return 0

        return (number_of_pitch * 3) / sum_innings_pitched


class CalculateTeamSabr:
    def team_der(
            self,
            batters_faced,
            suffer_hit,
            suffer_home_run,
            bb_hbp,
            strike_out,
            error):
        a = batters_faced - suffer_hit - bb_hbp - strike_out - error
        b = batters_faced - suffer_home_run - bb_hbp - strike_out

        if b == 0:
            return 0

        return a / b
