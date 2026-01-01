"""投手のセイバーメトリクス指標計算

Notes:
    Noneが渡されるとエラーになる。
    パワプロ用なので犠飛、盗塁死、敬遠などは除外されている
"""


def innings_conversion_for_display(
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


def calculate_earned_runs_average(
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


def calculate_runs_average(sum_innings_pitched: float, run: int) -> float:
    """Calculate URA

    Args:
        sum_innings_pitched (float): 投球回数。
        run (int): 失点。

    Returns:
        float: URA = (失点 * 9 * 3) / (投球回 * 3)
    """
    return (run * 9 * 3) / sum_innings_pitched \
        if sum_innings_pitched > 0 else 0


def calculate_walks_plus_hits_per_inning_pitched(
        sum_innings_pitched: float,
        hit: int,
        bb_hbp: int) -> float:
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


def calculate_strike_out_per_bbhp(bb_hbp: int, strike_out: int) -> float:
    """Calculate K/BBHP

    Args:
        bb_hbp (int): 与四死球数。
        strike_out (int): 奪三振数。

    Returns:
        float: K/BBHP = 奪三振 / 与四死球数
    """
    return strike_out / bb_hbp if bb_hbp > 0 else 0


def calculate_strike_out_per_game(
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


def calculate_strike_out_percentage(
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


def calculate_bbhp_per_game(sum_innings_pitched: float, bb_hbp: int) -> float:
    """Calculate BBHP/9

    Args:
        sum_innings_pitched (float): 投球回数。
        bb_hbp (int): 与四死球数。

    Returns:
        float: BBHP/9 = (与四死球数 * 9 * 3) / (投球回数 * 3)
    """
    return (bb_hbp * 9 * 3) / sum_innings_pitched \
        if sum_innings_pitched > 0 else 0


def calculate_bbhp_percentage(batters_faced: int, bb_hbp: int) -> float:
    """Calculate BBHP%

    Args:
        batters_faced (int): 対戦打者数。
        bb_hbp (int): 与四死球数。

    Returns:
        float: BBHP% = 与四死球数 / 対戦打者数
    """
    return bb_hbp / batters_faced \
        if batters_faced > 0 else 0


def calculate_hit_per_game(sum_innings_pitched: float, hit: int) -> float:
    """Calculate H/9

    Args:
        sum_innings_pitched (float): 投球回数。
        hit (int): 被安打数。

    Returns:
        float: H/9 = (被安打数 * 9 * 3) / (投球回数 * 3)
    """
    return (hit * 9 * 3) / sum_innings_pitched \
        if sum_innings_pitched > 0 else 0


def calculate_hit_percentage(batters_faced: int, hit: int) -> float:
    """Calculate H%

    Args:
        batters_faced (int): 対戦打者数。
        hit (int): 被安打数。

    Returns:
        float: H% = 被安打数 / 対戦打者数
    """
    return hit / batters_faced \
        if batters_faced > 0 else 0


def calculate_home_run_per_game(
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


def calculate_home_run_percentage(batters_faced: int, home_run: int) -> float:
    """Calculate HR%

    Args:
        batters_faced (int): 対戦打者数。
        home_run (int): 被本塁打数。

    Returns:
        float: HR% = 被本塁打数 / 対戦打者数
    """
    return home_run / batters_faced \
        if batters_faced > 0 else 0


def calculate_left_on_base_percentage(
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


def calculate_pitch_per_inning(sum_innings_pitched: float,
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


def calculate_fielding_independent_pitching(
        sum_innings_pitched: float,
        home_run: int,
        bb_hbp: int,
        strike_out: int) -> float:
    """Calculate FIP

    Args:
        sum_innings_pitched (float): 投球回数
        home_run (int): 被本塁打
        bb_hbp (int): 与四死球
        strike_out (int): 奪三振数

    Returns:
        float: FIP = ((被本塁打 * 13 + 与四死球 * 3 - 奪三振数 * 2) * 3) / (投球回数 * 3)
    """
    return ((home_run * 13 + bb_hbp * 3 - strike_out * 2) * 3) / \
        sum_innings_pitched + 3.0 if sum_innings_pitched > 0 else 0.0


def calculate_fip_subtracting_era(
        fip: float,
        era: float) -> float:
    """FIP substracting ERA

    Args:
        fip (float): FIP
        era (float): ERA: 防御率

    Returns:
        float: FIP - ERA
    
    Notes:
        FIP-ERA<0であれば、防御率が改善する可能性がある
        FIP-ERA>0であれば、防御率が悪化する可能性がある
    """
    return fip - era

