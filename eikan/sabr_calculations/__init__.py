"""セイバーメトリクス計算モジュール

打者、投手、チームの各種指標を計算する関数群を提供します。
"""

from .fielder import (
    calculate_total_bases,
    calculate_slugging_percentage,
    calculate_on_base_percentage,
    calculate_on_base_plus_slugging,
    calculate_batting_runs,
    calculate_weighted_on_base_average,
    calculate_gross_production_average,
    calculate_batting_average,
    calculate_bb_hp_percentage,
    calculate_isolated_discipline,
    calculate_isolated_power,
    calculate_bb_hbp_per_so,
    calculate_power_speed_number,
)

from .pitcher import (
    innings_conversion_for_display,
    innings_conversion_for_calculate,
    calculate_earned_runs_average,
    calculate_runs_average,
    calculate_walks_plus_hits_per_inning_pitched,
    calculate_strike_out_per_bbhp,
    calculate_strike_out_per_game,
    calculate_strike_out_percentage,
    calculate_bbhp_per_game,
    calculate_bbhp_percentage,
    calculate_hit_per_game,
    calculate_hit_percentage,
    calculate_home_run_per_game,
    calculate_home_run_percentage,
    calculate_left_on_base_percentage,
    calculate_pitch_per_inning,
    calculate_fielding_independent_pitching,
    calculate_fip_subtracting_era,
)

from .team import (
    calculate_team_der,
)

__all__ = [
    # 打者指標
    'calculate_total_bases',
    'calculate_slugging_percentage',
    'calculate_on_base_percentage',
    'calculate_on_base_plus_slugging',
    'calculate_batting_runs',
    'calculate_weighted_on_base_average',
    'calculate_gross_production_average',
    'calculate_batting_average',
    'calculate_bb_hp_percentage',
    'calculate_isolated_discipline',
    'calculate_isolated_power',
    'calculate_bb_hbp_per_so',
    'calculate_power_speed_number',
    # 投手指標
    'innings_conversion_for_display',
    'innings_conversion_for_calculate',
    'calculate_earned_runs_average',
    'calculate_runs_average',
    'calculate_walks_plus_hits_per_inning_pitched',
    'calculate_strike_out_per_bbhp',
    'calculate_strike_out_per_game',
    'calculate_strike_out_percentage',
    'calculate_bbhp_per_game',
    'calculate_bbhp_percentage',
    'calculate_hit_per_game',
    'calculate_hit_percentage',
    'calculate_home_run_per_game',
    'calculate_home_run_percentage',
    'calculate_left_on_base_percentage',
    'calculate_pitch_per_inning',
    'calculate_fielding_independent_pitching',
    'calculate_fip_subtracting_era',
    # チーム指標
    'calculate_team_der',
]

