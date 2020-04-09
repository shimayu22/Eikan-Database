class CalculateFielderSabr:
    """打者のセイバーメトリクスの指標を計算する

    Notes:
        Noneが渡されるとエラーになる
        パワプロ用なので犠飛、盗塁死、敬遠などは除外されている
    """

    def total_bases(
            self,
            hit: int,
            twobase: int,
            threebase: int,
            homerun: int) -> int:
        """Calculate Total Bases

        Args:
            hit (int): 安打数。
            twobase (int): 二塁打数。
            threebase (int): 三塁打数。
            homerun (int): 本塁打数。

        Returns:
            int: 塁打 = 安打 + 二塁打 + 三塁打 * 2 + 本塁打 * 3
        """
        return hit + twobase + threebase * 2 + homerun * 3

    def slugging_percentage(self, at_bat: int, tb: int) -> float:
        """Calculate SLG

        Args:
            at_bat (int): 打数。
            tb (int): 塁打。

        Returns:
            float: 長打率 = 塁打 / 打数
        """
        return tb / at_bat \
            if at_bat > 0 else 0

    def on_base_percentage(self, at_bat: int, bb_hbp: int, hit: int) -> float:
        """Calculate OBP

        Args:
            at_bat (int): 打数。
            bb_hbp (int): 四死球。
            hit (int): 安打数。

        Returns:
            float: 出塁率 = (安打数 + 四死球) / (打数 + 四死球)

        Notes:
            栄冠ナインの仕様上、犠飛を除外
        """
        return (hit + bb_hbp) / (at_bat + bb_hbp) \
            if (at_bat + bb_hbp) > 0 else 0

    def on_base_plus_slugging(self, obp: float, slg: float) -> float:
        """Calculate OPS

        Args:
            obp (float): 出塁率。
            slg (float): 長打率。

        Returns:
            float: OPS = OBP + SLG
        """
        return obp + slg

    def batting_runs(
            self,
            hit: int,
            twobase: int,
            threebase: int,
            homerun: int,
            bb_hbp: int,
            at_bat: int) -> float:
        """Calculate Butting Runs

        Args:
            hit (int): 安打数。
            twobase (int): 二塁打数。
            threebase (int): 三塁打数。
            homerun (int): 本塁打数。
            bb_hbp (int): 四死球。
            at_bat (int): 打数。

        Returns:
            float: BR = 0.44 * (安打 - 二塁打 - 三塁打 - 本塁打) + 0.77 * 二塁打 + \
                                1.12 * 三塁打 + 1.41 * 本塁打 + \
                                    0.29 * 四死球 - 0.25 * (打数 - 安打)
        Notes:
            栄冠ナインの仕様上、盗塁、盗塁刺を除外
        """
        return 0.44 * (hit - twobase - threebase - homerun) + 0.77 * twobase + \
            1.12 * threebase + 1.41 * homerun + \
            0.29 * bb_hbp - 0.25 * (at_bat - hit)

    def weighted_on_base_average(
            self,
            hit: int,
            twobase: int,
            threebase: int,
            homerun: int,
            bb_hbp: int,
            at_bat: int) -> float:
        """Calculate wOBA

        Args:
            hit (int): 安打数。
            twobase (int): 二塁打数。
            threebase (int): 三塁打数。
            homerun (int): 本塁打数。
            bb_hbp (int): 四死球。
            at_bat (int): 打数。

        Returns:
            float: (0.7 * 四死球 + 0.9 * (安打 - 二塁打 - 三塁打 - 本塁打) + \
                    1.3 * 二塁打 + 1.6 * 三塁打 + 2.0 * 本塁打) / (打数 + 四死球)
        Notes:
            栄冠ナインの仕様上、犠飛を除外
        """
        return (0.7 * bb_hbp + 0.9 * (hit - twobase - threebase - homerun) + 1.3 * twobase +
                1.6 * threebase + 2.0 * homerun) / (at_bat + bb_hbp) \
            if (at_bat + bb_hbp) > 0 else 0

    def gross_production_average(self, obp: float, slg: float) -> float:
        """Calculate GPA

        Args:
            obp (float): 出塁率。
            slg (float): 長打率。

        Returns:
            float: GPA = (OBP * 1.8 + SLG) / 4
        """
        return (obp * 1.8 + slg) / 4

    def batting_average(self, at_bat: int, hit: int) -> float:
        """Calculate AVG

        Args:
            at_bat (int): 打数。
            hit (int): 安打数。

        Returns:
            float: 打率 = 安打数 / 打数
        """
        return hit / at_bat \
            if at_bat > 0 else 0

    def bb_hp_percentage(self, at_bat: int, bb_hbp: int, bunt: int) -> float:
        """Calculate BBHP%

        Args:
            at_bat (int): 打数。
            bb_hbp (int): 四死球数。
            bunt (int): 犠打数。

        Returns:
            float: 四死球率 = 四死球 / (打数 + 四死球数 + 犠打数)
        Notes:
            打席 = 打数 + 四死球数 + 犠打数
            栄冠ナインの仕様上、犠飛を除外
        """

        return bb_hbp / (at_bat + bb_hbp + bunt) \
            if (at_bat + bb_hbp + bunt) > 0 else 0

    def isolated_discipline(self, obp: float, avg: float) -> float:
        """Calculate IsoD

        Args:
            obp (float): 出塁率。
            avg (float): 打率。

        Returns:
            float: IsoD = 出塁率 -　打率
        """
        return obp - avg

    def isolated_power(self, slg: float, avg: float) -> float:
        """Calculate IsoP

        Args:
            slg (float): 長打率。
            avg (float): 打率。

        Returns:
            float: IsoP = 長打率 - 打率
        """
        return slg - avg

    def bb_hbp_per_so(self, strike_out: int, bb_hbp: int) -> float:
        """Calculate BBHP/K

        Args:
            strike_out (int): 三振数
            bb_hbp (int): 四死球数

        Returns:
            float: BBHP/K = 四死球数 / 三振数
        """
        return bb_hbp / strike_out \
            if strike_out > 0 else 0

    def power_speed_number(self, home_run: int, stolen_base: int) -> float:
        """Calculate P-S

        Args:
            home_run (int): 本塁打数
            stolen_base (int): 盗塁数

        Returns:
            float: P-S = (本塁打数 * 盗塁数 * 2) / (本塁打数 + 盗塁数)
        """

        return (home_run * stolen_base * 2) / (home_run + stolen_base) \
            if (home_run + stolen_base) > 0 else 0


class CalculatePitcherSabr:
    """投手のセイバーメトリクスの指標を計算する

    Notes:
        Noneが渡されるとエラーになる。
        パワプロ用なので犠飛、盗塁死、敬遠などは除外されている
    """

    def innings_conversion_for_display(
            self,
            innings_pitched: int,
            innings_pitched_fraction: int) -> float:
        """表示用に「178.2」という値に変換する ex) 178回2/3の場合:

        Args:
            innings_pitched (int): 投球回数(178)
            innings_pitched_fraction (int): 投球回数(2)

        Returns:
            float: 投球回数 = 178.2
        """

        innings = float(
            innings_pitched +
            innings_pitched_fraction // 3)
        outcount = innings_pitched_fraction % 3
        if outcount == 1:
            innings += 0.1
        elif outcount == 2:
            innings += 0.2

        return innings

    def innings_conversion_for_calculate(
            self,
            innings_pitched: int,
            innings_pitched_fraction: int) -> float:
        """計算用に「178.666... * 3」という値に変換する ex) 178回2/3の場合:

        Args:
            innings_pitched (int): 投球回数(178)
            innings_pitched_fraction (int): 投球回数(2)

        Returns:
            float: 投球回数 = 178.666... * 3
        """

        return (innings_pitched + innings_pitched_fraction / 3) * 3

    def earned_runs_average(
            self,
            sum_innings_pitched: float,
            earned_run: int) -> float:
        """Calculate ERA

        Args:
            sum_innings_pitched (float): 投球回数。
            earned_run (int): 自責点。

        Returns:
            float: ERA = (自責点 * 9 * 3) / (投球回 * 3)
        """
        return (earned_run * 9 * 3) / sum_innings_pitched \
            if sum_innings_pitched > 0 else 0

    def runs_average(self, sum_innings_pitched: float, run: int) -> float:
        """Calculate URA

        Args:
            sum_innings_pitched (float): 投球回数。
            run (int): 失点。

        Returns:
            float: URA = (失点 * 9 * 3) / (投球回 * 3)
        """
        return (run * 9 * 3) / sum_innings_pitched \
            if sum_innings_pitched > 0 else 0

    def walks_plus_hits_per_inning_pitched(
            self, sum_innings_pitched: float, hit: int, bb_hbp: int) -> float:
        """Calculate WHIP

        Args:
            sum_innings_pitched (float): 投球回数。
            hit (int): 被安打数。
            bb_hbp (int): 与四死球数。

        Returns:
            float: WHIP = ((被安打数 + 与四死球数) * 3) / (投球回数 * 3)
        """

        return ((hit + bb_hbp) * 3) / sum_innings_pitched \
            if sum_innings_pitched > 0 else 0

    def strike_out_per_bbhp(self, bb_hbp: int, strike_out: int) -> float:
        """Calculate K/BBHP

        Args:
            bb_hbp (int): 与四死球数。
            strike_out (int): 奪三振数。

        Returns:
            float: K/BBHP = 奪三振 / 与四死球数
        """
        return strike_out / bb_hbp \
            if bb_hbp > 0 else 0

    def strike_out_per_game(
            self,
            sum_innings_pitched: float,
            strike_out: int) -> float:
        """Calculate K/9

        Args:
            sum_innings_pitched (float): 投球回数。
            strike_out (int): 奪三振数。

        Returns:
            float: K/9 = (奪三振数 * 9 * 3) / (投球回数 * 3)
        """
        return (strike_out * 9 * 3) / sum_innings_pitched \
            if sum_innings_pitched > 0 else 0

    def strike_out_percentage(
            self,
            batters_faced: int,
            strike_out: int) -> float:
        """Calculate K%

        Args:
            batters_faced (int): 対戦打者数。
            strike_out (int): 奪三振数。

        Returns:
            float: K% = 奪三振数 / 対戦打者数
        """
        return strike_out / batters_faced \
            if batters_faced > 0 else 0

    def bbhp_per_game(self, sum_innings_pitched: float, bb_hbp: int) -> float:
        """Calculate BBHP/9

        Args:
            sum_innings_pitched (float): 投球回数。
            bb_hbp (int): 与四死球数。

        Returns:
            float: BBHP/9 = (与四死球数 * 9 * 3) / (投球回数 * 3)
        """
        return (bb_hbp * 9 * 3) / sum_innings_pitched \
            if sum_innings_pitched > 0 else 0

    def bbhp_percentage(self, batters_faced: int, bb_hbp: int) -> float:
        """Calculate BBHP%

        Args:
            batters_faced (int): 対戦打者数。
            bb_hbp (int): 与四死球数。

        Returns:
            float: BBHP% = 与四死球数 / 対戦打者数
        """
        return bb_hbp / batters_faced \
            if batters_faced > 0 else 0

    def hit_per_game(self, sum_innings_pitched: float, hit: int) -> float:
        """Calculate H/9

        Args:
            sum_innings_pitched (float): 投球回数。
            hit (int): 被安打数。

        Returns:
            float: H/9 = (被安打数 * 9 * 3) / (投球回数 * 3)
        """
        return (hit * 9 * 3) / sum_innings_pitched \
            if sum_innings_pitched > 0 else 0

    def hit_percentage(self, batters_faced: int, hit: int) -> float:
        """Calculate H%

        Args:
            batters_faced (int): 対戦打者数。
            hit (int): 被安打数。

        Returns:
            float: H% = 被安打数 / 対戦打者数
        """
        return hit / batters_faced \
            if batters_faced > 0 else 0

    def home_run_per_game(
            self,
            sum_innings_pitched: float,
            home_run: int) -> float:
        """Calculate HR/9

        Args:
            sum_innings_pitched (float): 投球回数。
            home_run (int): 被本塁打数。

        Returns:
            float: HR/9 = (被本塁打数 * 9 * 3) / (投球回数 * 3)
        """
        return (home_run * 9 * 3) / sum_innings_pitched \
            if sum_innings_pitched > 0 else 0

    def home_run_percentage(self, batters_faced: int, home_run: int) -> float:
        """Calculate HR%

        Args:
            batters_faced (int): 対戦打者数。
            home_run (int): 被本塁打数。

        Returns:
            float: HR% = 被本塁打数 / 対戦打者数
        """
        return home_run / batters_faced \
            if batters_faced > 0 else 0

    def left_on_base_percentage(
            self,
            hit: int,
            bb_hbp: int,
            home_run: int,
            run: int) -> float:
        """Calculate LOB%

        Args:
            hit (int): 被安打数。
            bb_hbp (int): 与四死球数。
            home_run (int): 被本塁打数。
            run (int): 失点。

        Returns:
            float: LOB% = (被安打数 + 与四死球数 - 失点) / (被安打数 + 与四死球数 - 1.4 * 被本塁打数)
        """
        return (hit + bb_hbp - run) / (hit + bb_hbp - 1.4 * home_run) \
            if (hit + bb_hbp - 1.4 * home_run) != 0.0 else 0

    def pitch_per_inning(self, sum_innings_pitched: float,
                         number_of_pitch: int) -> float:
        """Calculate P/IP

        Args:
            sum_innings_pitched (float): 投球回数。
            number_of_pitch (int): 投球数。

        Returns:
            float: P/IP = (投球数 * 3) / (投球回数 * 3)
        """
        return (number_of_pitch * 3) / sum_innings_pitched \
            if sum_innings_pitched > 0 else 0


class CalculateTeamSabr:
    """チームのセイバーメトリクスの指標を計算する

    Notes:
        Noneが渡されるとエラーになる
        パワプロ用なので犠飛、盗塁死、敬遠などは除外されている
    """

    def team_der(
            self,
            batters_faced: int,
            suffer_hit: int,
            suffer_home_run: int,
            bb_hbp: int,
            strike_out: int,
            error: int) -> float:
        """Calculate Team DER

        Args:
            batters_faced (int): 対戦打者数。
            suffer_hit (int): 被安打数。
            suffer_home_run (int): 被本塁打数。
            bb_hbp (int): 与四死球数。
            strike_out (int): 奪三振数。
            error (int): エラー数。

        Returns:
            float: DER = (対戦打者数 - 被安打数 - 与四死球数 - 奪三振数 - エラー数) / (対戦打者数 - 被本塁打数 - 与四死球数 - 奪三振数)
        """
        a = batters_faced - suffer_hit - bb_hbp - strike_out - error
        b = batters_faced - suffer_home_run - bb_hbp - strike_out

        return a / b if b > 0 else 0
