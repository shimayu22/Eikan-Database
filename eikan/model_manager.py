"""Modelsで使用する処理の集まり

Notes:
    SavedValueExtractor:save()で使用する処理
    ChoicesFormatter:CHOICESを辞書型に変換する処理
"""
from eikan import defaults


class SavedValueExtractor:
    """save時に行う処理"""

    def create_game_results(self, score: int, run: int) -> int:
        """試合結果（勝負分）を判定する

        Args:
            score (int): 自チームの得点
            run (int): 相手チームの得点

        Returns:
            int: 1（勝）,2（負）,3（分）を返す
        """
        result_choices = defaults.result_choices_to_dict()
        return result_choices['勝'] if score > run else result_choices['負'] if score < run else result_choices['分']

    def update_is_pitcher(self, position: int, is_pitched: bool) -> bool:
        """Players保存時に投手または野手で登板したかを判定する

        Args:
            position (int): ポジション
            is_pitched (bool): 野手で登板があったか

        Returns:
            bool: 投手または登板したことがある野手かを返す

        Notes:
            is_pitcherがTrueの場合、pitcher_resultsのプルダウンに表示される
        """
        position_choices = defaults.position_choices_to_dict()
        return position == position_choices['投'] or is_pitched
    
    def check_is_cold_game(self, is_cold_game: bool, competition_type: int, competition_round: int) -> bool:
        """Games保存時に、コールドゲームになりうる試合か判定する

        Args:
            is_cold_game (bool): 入力されたis_cold_game
            competition_type (int): 大会
            competition_round (int): 回戦

        Returns:
            bool: 判定後のis_cold_game
        
        Notes:
            県大会決勝、甲子園、センバツの場合はFalseを返す
        """
        competition_choices = defaults.competition_choices_to_dict()
        round_choices = defaults.round_choices_to_dict()
        
        if not is_cold_game:
            return False
        
        if competition_type >= competition_choices['甲子園']:
            return False
        
        if competition_type == competition_choices['県大会'] and competition_round == round_choices['決勝']:
            return False
        
        return True


class ChoicesFormatter:
    """ ModelsのCHOICESを辞書型にしてkeyとvaluesを入れ替えて返す 
    
    Notes:
        互換性のために残しています。新しいコードでは defaults モジュールの関数を直接使用してください。
    """

    @staticmethod
    def competition_choices_to_dict() -> dict:
        """COMPETITION_CHOICESを返す

        Returns:
            dict: {'選択': '', '練習試合': 1, '県大会': 2, '地区大会': 3, '全国大会': 4, '甲子園': 5, 'センバツ': 6}
        """
        return defaults.competition_choices_to_dict()

    @staticmethod
    def round_choices_to_dict() -> dict:
        """ROUND_CHOICESを返す

        Returns:
            dict: {'選択': '', '練習試合': 1, '1回戦': 2, '2回戦': 3, '3回戦': 4, '準々決勝': 5, '準決勝': 6, '決勝': 7}
        """
        return defaults.round_choices_to_dict()

    @staticmethod
    def result_choices_to_dict() -> dict:
        """RESULT_CHOICESを返す

        Returns:
            dict: {'選択': '', '勝': 1, '負': 2, '分': 3}
        """
        return defaults.result_choices_to_dict()

    @staticmethod
    def rank_choices_to_dict() -> dict:
        """RANK_CHOICESを返す

        Returns:
            dict: {'選択': '', '弱小': 1, 'そこそこ': 2, '中堅': 3, '強豪': 4, '名門': 5}
        """
        return defaults.rank_choices_to_dict()

    @staticmethod
    def period_choices_to_dict() -> dict:
        """PERIOD_CHOICESを返す

        Returns:
            dict: {'選択': '', '夏': 1, '秋': 2}
        """
        return defaults.period_choices_to_dict()

    @staticmethod
    def position_choices_to_dict() -> dict:
        """POSITION_CHOICESを返す

        Returns:
            dict: {'選択': '', '投': 1, '捕': 2, '一': 3, '二': 4, '三': 5, '遊': 6, '外': 7}
        """
        return defaults.position_choices_to_dict()
