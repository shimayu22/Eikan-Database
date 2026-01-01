"""チームのセイバーメトリクス指標計算

Notes:
    Noneが渡されるとエラーになる
    パワプロ用なので犠飛、盗塁死、敬遠などは除外されている
"""


def calculate_team_der(
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

