"""Djangoモデルのdefault値とlimit_choices_toを動的に設定する関数群

Notes:
    循環importを回避するため、django.apps.apps.get_model()を使用してモデルを取得している
"""
from django.apps import apps
from eikan.constants import (
    DEFAULT_START_YEAR_TEAMS,
    DEFAULT_START_YEAR_PLAYERS,
    YEARS_BACK_FOR_SUMMER,
    YEARS_BACK_FOR_AUTUMN,
)


# ============================================================================
# Choices を辞書型に変換する関数群
# ============================================================================

def competition_choices_to_dict() -> dict:
    """COMPETITION_CHOICESを返す
    
    Returns:
        dict: {'選択': '', '練習試合': 1, '県大会': 2, '地区大会': 3, '全国大会': 4, '甲子園': 5, 'センバツ': 6}
    """
    Games = apps.get_model('eikan', 'Games')
    return {v: k for k, v in dict(Games.COMPETITION_CHOICES).items()}


def round_choices_to_dict() -> dict:
    """ROUND_CHOICESを返す
    
    Returns:
        dict: {'選択': '', '練習試合': 1, '1回戦': 2, '2回戦': 3, '3回戦': 4, '準々決勝': 5, '準決勝': 6, '決勝': 7}
    """
    Games = apps.get_model('eikan', 'Games')
    return {v: k for k, v in dict(Games.ROUND_CHOICES).items()}


def result_choices_to_dict() -> dict:
    """RESULT_CHOICESを返す
    
    Returns:
        dict: {'選択': '', '勝': 1, '負': 2, '分': 3}
    """
    Games = apps.get_model('eikan', 'Games')
    return {v: k for k, v in dict(Games.RESULT_CHOICES).items()}


def rank_choices_to_dict() -> dict:
    """RANK_CHOICESを返す
    
    Returns:
        dict: {'選択': '', '弱小': 1, 'そこそこ': 2, '中堅': 3, '強豪': 4, '名門': 5}
    """
    Games = apps.get_model('eikan', 'Games')
    return {v: k for k, v in dict(Games.RANK_CHOICES).items()}


def period_choices_to_dict() -> dict:
    """PERIOD_CHOICESを返す
    
    Returns:
        dict: {'選択': '', '夏': 1, '秋': 2}
    """
    Teams = apps.get_model('eikan', 'Teams')
    return {v: k for k, v in dict(Teams.PERIOD_CHOICES).items()}


def position_choices_to_dict() -> dict:
    """POSITION_CHOICESを返す
    
    Returns:
        dict: {'選択': '', '投': 1, '捕': 2, '一': 3, '二': 4, '三': 5, '遊': 6, '外': 7}
    """
    Players = apps.get_model('eikan', 'Players')
    return {v: k for k, v in dict(Players.POSITION_CHOICES).items()}


# ============================================================================
# Teams モデルのdefault値を設定する関数群
# ============================================================================

def create_default_year_for_teams() -> int:
    """Teamsのyearのdefaultを設定する
    
    Returns:
        int: 前チームの期間(period)が夏(1)なら前チームと同じ年、秋(2)なら翌年を返す
    
    Notes:
        初めて登録する場合はDEFAULT_START_YEAR_TEAMSを返す
    """
    Teams = apps.get_model('eikan', 'Teams')
    if not Teams.objects.exists():
        return DEFAULT_START_YEAR_TEAMS
    
    latest_team = Teams.objects.latest('pk')
    period_choices = period_choices_to_dict()
    return latest_team.year if latest_team.period == period_choices['夏'] else latest_team.year + 1


def create_default_period() -> int:
    """Teamsのperiodのdefaultを設定する
    
    Returns:
        int: 前チームの期間(period)が夏(1)なら秋(2)、秋(2)なら夏(1)を返す
    
    Notes:
        初めて登録する場合は1を返す
    """
    Teams = apps.get_model('eikan', 'Teams')
    if not Teams.objects.exists():
        return 1
    
    period_choices = period_choices_to_dict()
    return 1 if Teams.objects.latest('pk').period == period_choices['秋'] else 2


def create_default_prefecture() -> int:
    """Teamsのprefectureのdefaultを設定する
    
    Returns:
        int: 前のチームと同じ都道府県を返す
    
    Notes:
        初めて登録する場合は0を返す
    """
    Teams = apps.get_model('eikan', 'Teams')
    return 0 if not Teams.objects.exists() else Teams.objects.latest('pk').prefecture


# ============================================================================
# Players モデルのdefault値を設定する関数群
# ============================================================================

def create_default_year_for_players() -> int:
    """Playersのadmission_yearのdefaultを設定する
    
    Returns:
        int: 現在のチームのyearを返す
    
    Notes:
        初めて登録する場合はDEFAULT_START_YEAR_PLAYERSを返す
    """
    Teams = apps.get_model('eikan', 'Teams')
    return Teams.objects.latest('pk').year if Teams.objects.exists() else DEFAULT_START_YEAR_PLAYERS


# ============================================================================
# Games モデルのdefault値を設定する関数群
# ============================================================================

def create_default_team_id() -> int:
    """Gamesのteam_idのdefaultを設定する
    
    Returns:
        int: 現在のチームのidを返す
    
    Notes:
        Teamsにレコードがなければ''を返す
    """
    Teams = apps.get_model('eikan', 'Teams')
    return Teams.objects.latest('pk').id if Teams.objects.exists() else ''


def create_default_competition_type() -> int:
    """Gamesのcompetition_typeのdefaultを設定する
    
    Returns:
        int: 1つ前の試合と同じcompetition_typeを返す
    
    Notes:
        一つ前が練習試合の場合は2(県大会)を返す
        次の大会へ進む条件を満たせば、次の大会を返す
    """
    Teams = apps.get_model('eikan', 'Teams')
    Games = apps.get_model('eikan', 'Games')
    
    competition_choices = competition_choices_to_dict()
    competition_round_choices = round_choices_to_dict()
    result_choices = result_choices_to_dict()
    period_choices = period_choices_to_dict()
    
    if not Teams.objects.exists() or not Games.objects.exists():
        return competition_choices['県大会']
    
    team = Teams.objects.latest('pk')
    if not Games.objects.filter(team_id=team).exists():
        return competition_choices['県大会']
    else:
        game = Games.objects.select_related('team_id').filter(team_id=team).latest('pk')
    
    if game.competition_type == competition_choices['練習試合']:
        return competition_choices['県大会']
    
    if team.period == period_choices['秋']:
        if game.competition_type == competition_choices['県大会'] and \
                game.competition_round == competition_round_choices['2回戦'] and \
                game.result == result_choices['勝']:
            return competition_choices['地区大会']
        
        if game.competition_type == competition_choices['地区大会'] and \
                game.competition_round == competition_round_choices['2回戦'] and \
                game.result == result_choices['勝']:
            return competition_choices['全国大会']
        
        if game.competition_type == competition_choices['全国大会'] and \
            game.result == result_choices['負']:
            return competition_choices['センバツ']
        
        if game.competition_type == competition_choices['全国大会'] and \
            game.competition_round == competition_round_choices['決勝'] and \
            game.result == result_choices['勝']:
            return competition_choices['センバツ']
    
    else:
        if game.competition_type == competition_choices['県大会'] and \
                game.competition_round == competition_round_choices['決勝'] and \
                game.result == result_choices['勝']:
            return competition_choices['甲子園']
    
    if game.result == result_choices['負']:
        return competition_choices['県大会']
    
    return game.competition_type


def create_default_competition_round() -> int:
    """Gamesのcompetition_roundのdefaultを設定する
    
    Returns:
        int: 前の試合が勝なら次の試合のcompetition_typeを返す
    
    Notes:
        一つ前が練習試合または負の場合は2(1回戦)を返す
        １回戦、３回戦がない場合は考慮していない
        秋の大会は考慮している
    """
    Teams = apps.get_model('eikan', 'Teams')
    Games = apps.get_model('eikan', 'Games')
    
    competition_choices = competition_choices_to_dict()
    competition_round_choices = round_choices_to_dict()
    result_choices = result_choices_to_dict()
    period_choices = period_choices_to_dict()
    
    if not Teams.objects.exists() or not Games.objects.exists():
        return competition_round_choices['1回戦']
    
    team = Teams.objects.latest('pk')
    if not Games.objects.filter(team_id=team).exists():
        return competition_round_choices['1回戦']
    else:
        game = Games.objects.select_related('team_id').filter(team_id=team).latest('pk')
    
    if game.competition_type == competition_choices['練習試合']:
        return competition_round_choices['1回戦']
    
    if game.result == result_choices['負']:
        return competition_round_choices['1回戦']
    
    if game.competition_round == competition_round_choices['決勝']:
        return competition_round_choices['1回戦']
    
    if team.period == period_choices['秋']:
        if game.competition_type == competition_choices['県大会'] and \
                game.competition_round == competition_round_choices['2回戦']:
            return competition_round_choices['1回戦']
        
        if game.competition_type == competition_choices['地区大会'] and \
                game.competition_round == competition_round_choices['2回戦']:
            if game.result == result_choices['勝']:
                return competition_round_choices['2回戦']
            else:
                return competition_round_choices['1回戦']
        
        if game.competition_type == competition_choices['全国大会'] and \
                game.competition_round == competition_round_choices['2回戦']:
            if game.result == result_choices['勝']:
                return competition_round_choices['準決勝']
    
    return game.competition_round + 1


def create_default_team_rank() -> int:
    """Gamesのrankのdefaultを設定する
    
    Returns:
        int: １つ前のレコードと同じrankを返す
    
    Notes:
        初めて登録する場合は0を返す
    """
    Games = apps.get_model('eikan', 'Games')
    return Games.objects.latest('pk').rank if Games.objects.exists() else 0


# ============================================================================
# FielderResults/PitcherResults モデルのlimit_choices_toを設定する関数群
# ============================================================================

def select_display_players() -> dict:
    """fielder_resultsのplayer_idのlimit_choices_toを設定する
    
    Returns:
        dict: 現在のチームの年度と期間をもとに、そのチームに所属している選手を表示する
        夏: ３学年分
        秋: ２学年分
    
    Notes:
        ModelSettingsのis_used_limit_choices_toがTrueの場合、全ての選手を表示する
    """
    Teams = apps.get_model('eikan', 'Teams')
    ModelSettings = apps.get_model('eikan', 'ModelSettings')
    
    # ModelSettingsの存在チェックと設定取得を1回のクエリで実行
    if ModelSettings.objects.exists():
        latest_setting = ModelSettings.objects.latest('pk')
        if latest_setting.is_used_limit_choices_to:
            return {}
    
    if not Teams.objects.exists():
        return {}
    
    period_choices = period_choices_to_dict()
    teams = Teams.objects.latest('pk')
    if teams.period == period_choices['夏']:
        return {
            "admission_year__gte": teams.year - YEARS_BACK_FOR_SUMMER,
            "admission_year__lte": teams.year}
    else:
        return {
            "admission_year__gte": teams.year - YEARS_BACK_FOR_AUTUMN,
            "admission_year__lte": teams.year}


def select_display_pitchers() -> dict:
    """pitcher_resultsのplayer_idのlimit_choices_toを設定する
    
    Returns:
        dict: 現在のチームの年度と期間をもとに、そのチームに所属している投手を表示する
        夏: ３学年分
        秋: ２学年分
    
    Notes:
        - 投手または登板した野手のみ表示される
        - ModelSettingsのis_used_limit_choices_toがTrueの場合、全ての投手を表示する
    """
    Teams = apps.get_model('eikan', 'Teams')
    ModelSettings = apps.get_model('eikan', 'ModelSettings')
    
    # ModelSettingsの存在チェックと設定取得を1回のクエリで実行
    if ModelSettings.objects.exists():
        latest_setting = ModelSettings.objects.latest('pk')
        if latest_setting.is_used_limit_choices_to:
            return {"is_pitcher": True}
    
    if not Teams.objects.exists():
        return {"is_pitcher": True}
    
    period_choices = period_choices_to_dict()
    teams = Teams.objects.latest('pk')
    if teams.period == period_choices['夏']:
        return {
            "is_pitcher": True,
            "admission_year__gte": teams.year - YEARS_BACK_FOR_SUMMER,
            "admission_year__lte": teams.year}
    else:
        return {
            "is_pitcher": True,
            "admission_year__gte": teams.year - YEARS_BACK_FOR_AUTUMN,
            "admission_year__lte": teams.year}

