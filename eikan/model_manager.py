"""Modelsで使用する処理の集まり

Notes:
    DefaultValueExtractor:defaultやchoicesで使用する処理
    SavedValueExtractor:save()で使用する処理
"""


class DefaultValueExtractor:
    """defaultやchoicesを動的に設定する"""
    @staticmethod
    def create_default_year_for_teams() -> int:
        """Teamsのyearのdefaultを設定する

        Returns:
            int: 前チームの期間(period)が夏(1)なら前チームと同じ年、秋(2)なら翌年を返す

        Notes:
            初めて登録する場合は1941を返す
        """
        from eikan.models import Teams
        if not Teams.objects.exists():
            return 1941

        period = Teams.objects.latest('pk').period
        this_year = Teams.objects.latest('pk').year
        return this_year if period == 1 else this_year + 1

    @staticmethod
    def create_default_period() -> int:
        """Teamsのperiodのdefaultを設定する

        Returns:
            int: 前チームの期間(period)が夏(1)なら秋(2)、秋(2)なら夏(1)を返す

        Notes:
            初めて登録する場合は1を返す
        """
        from eikan.models import Teams
        if not Teams.objects.exists():
            return 1

        return 1 if Teams.objects.latest('pk').period == 2 else 2

    @staticmethod
    def create_default_prefecture() -> int:
        """Teamsのprefectureのdefaultを設定する

        Returns:
            int: 前のチームと同じ都道府県を返す

        Notes:
            初めて登録する場合は0を返す
        """
        from eikan.models import Teams
        return 0 if not Teams.objects.exists() else Teams.objects.latest('pk').prefecture

    @staticmethod
    def create_default_year_for_players() -> int:
        """Playersのadmission_yearのdefaultを設定する

        Returns:
            int: 現在のチームのyearを返す

        Notes:
            初めて登録する場合は1939を返す
        """
        from eikan.models import Teams
        return Teams.objects.latest(
            'pk').year if Teams.objects.exists() else 1939

    @staticmethod
    def create_default_team_id() -> int:
        """Gamesのteam_idのdefaultを設定する

        Returns:
            int: 現在のチームのidを返す

        Notes:
            Teamsにレコードがなければ0を返す
        """
        from eikan.models import Teams
        return Teams.objects.latest('pk').id if Teams.objects.exists() else 0

    @staticmethod
    def create_default_competition_type() -> int:
        """Gamesのcompetition_typeのdefaultを設定する

        Returns:
            int: 1つ前の試合と同じcompetition_typeを返す

        Notes:
            一つ前が練習試合の場合は2(県大会)を返す
        """
        from eikan.models import Teams, Games

        competition_choices = ChoicesFormatter.competition_choices_to_dict()
        competition_round_choices = ChoicesFormatter.round_choices_to_dict()
        result_choices = ChoicesFormatter.result_choices_to_dict()
        period_choices = ChoicesFormatter.period_choices_to_dict()

        if not Teams.objects.exists() or not Games.objects.exists():
            return competition_choices['県大会']

        team = Teams.objects.latest('pk')
        if not Games.objects.filter(team_id=team).exists():
            return competition_choices['県大会']
        else:
            game = Games.objects.select_related(
                'team_id').filter(team_id=team).latest('pk')

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
                return competition_choices['センバツ']
        else:
            if game.competition_type == competition_choices['県大会'] and \
                    game.competition_round == competition_round_choices['決勝'] and \
                    game.result == result_choices['勝']:
                return competition_choices['甲子園']

        return game.competition_type

    @staticmethod
    def create_default_team_rank() -> int:
        """Gamesのrankのdefaultを設定する

        Returns:
            int: １つ前のレコードと同じrankを返す

        Notes:
            初めて登録する場合は0を返す
        """
        from eikan.models import Games
        return Games.objects.latest('pk').rank if Games.objects.exists() else 0

    @staticmethod
    def select_display_players() -> dict:
        """fielder_resultsのplayer_idのlimit_choices_toを設定する

        Returns:
            dict: 現在のチームの年度と期間をもとに、そのチームに所属している選手を表示する
            夏: ３学年分
            秋: ２学年分

        Notes:
            ModelSettingsのis_used_limit_choices_toがTrueの場合、全ての選手を表示する
        """
        from eikan.models import Teams, ModelSettings

        if ModelSettings.objects.exists() and ModelSettings.objects.latest(
                'pk').is_used_limit_choices_to:
            return {}

        if not Teams.objects.exists():
            return {}

        teams = Teams.objects.latest('pk')
        if teams.period == 1:
            return {
                "admission_year__gte": teams.year - 2,
                "admission_year__lte": teams.year}
        else:
            return {
                "admission_year__gte": teams.year - 1,
                "admission_year__lte": teams.year}

    @staticmethod
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
        from eikan.models import Teams, ModelSettings

        if ModelSettings.objects.exists() and ModelSettings.objects.latest(
                'pk').is_used_limit_choices_to:
            return {"is_pitcher": True}

        if not Teams.objects.exists():
            return {"is_pitcher": True}

        teams = Teams.objects.latest('pk')
        if teams.period == 1:
            return {
                "is_pitcher": True,
                "admission_year__gte": teams.year - 2,
                "admission_year__lte": teams.year}
        else:
            return {
                "is_pitcher": True,
                "admission_year__gte": teams.year - 1,
                "admission_year__lte": teams.year}


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
        return 1 if score > run else 2 if score < run else 3

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
        return position == 1 or is_pitched


class ChoicesFormatter:
    """ ModelsのCHOICESを辞書型にしてkeyとvaluesを入れ替えて返す """
    from django.db import models

    @staticmethod
    def competition_choices_to_dict() -> dict:
        """COMPETITION_CHOICESを返す

        Returns:
            dict: {'選択': '', '練習試合': 1, '県大会': 2, '地区大会': 3, '甲子園': 4, 'センバツ': 5}
        """
        from eikan.models import Games
        return {v: k for k, v in dict(Games.COMPETITION_CHOICES).items()}

    @staticmethod
    def round_choices_to_dict() -> dict:
        """ROUND_CHOICESを返す

        Returns:
            dict: {'選択': '', '練習試合': 1, '1回戦': 2, '2回戦': 3, '3回戦': 4, '準々決勝': 5, '準決勝': 6, '決勝': 7}
        """
        from eikan.models import Games
        return {v: k for k, v in dict(Games.ROUND_CHOICES).items()}

    @staticmethod
    def result_choices_to_dict() -> dict:
        """RESULT_CHOICESを返す

        Returns:
            dict: {'選択': '', '勝': 1, '負': 2, '分': 3}
        """
        from eikan.models import Games
        return {v: k for k, v in dict(Games.RESULT_CHOICES).items()}

    @staticmethod
    def rank_choices_to_dict() -> dict:
        """RANK_CHOICESを返す

        Returns:
            dict: {'選択': '', '弱小': 1, 'そこそこ': 2, '中堅': 3, '強豪': 4, '名門': 5}
        """
        from eikan.models import Games
        return {v: k for k, v in dict(Games.RANK_CHOICES).items()}

    @staticmethod
    def period_choices_to_dict() -> dict:
        """PERIOD_CHOICESを返す

        Returns:
            dict: {'選択': '', '夏': 1, '秋': 2}
        """
        from eikan.models import Teams
        return {v: k for k, v in dict(Teams.PERIOD_CHOICES).items()}

    @staticmethod
    def position_choices_to_dict() -> dict:
        """POSITION_CHOICESを返す

        Returns:
            dict: {'選択': '', '投': 1, '捕': 2, '一': 3, '二': 4, '三': 5, '遊': 6, '外': 7}
        """
        from eikan.models import Players
        return {v: k for k, v in dict(Players.POSITION_CHOICES).items()}
