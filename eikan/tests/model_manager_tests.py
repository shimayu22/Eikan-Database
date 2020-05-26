from django.test import TestCase
from eikan.models import Teams, Games, ModelSettings
from eikan.model_manager import DefaultValueExtractor, SavedValueExtractor, ChoicesFormatter


class DefaultValueExtractorTests(TestCase):
    def test_create_default_year_for_teams(self):
        """
        Teamsにレコードが存在しない場合 -> 1941(初期値)
        Teamsにレコードが存在して、最新レコードが
            period == 1(夏) -> 同じyearを返す
            period == 2(秋) -> 次のyearを返す
        """
        self.assertEqual(
            DefaultValueExtractor.create_default_year_for_teams(), 1941)
        Teams(year=1985, period=1).save()
        self.assertEqual(
            DefaultValueExtractor.create_default_year_for_teams(), 1985)
        Teams(year=1985, period=2).save()
        self.assertEqual(
            DefaultValueExtractor.create_default_year_for_teams(), 1986)

    def test_create_default_period(self):
        """
        Teamsにレコードが存在しない場合 -> 1(夏:初期値)
        Teamsにレコードが存在して、最新レコードが
            period == 1(夏) -> 2(秋)を返す
            period == 2(秋) -> 1(夏)を返す
        """
        self.assertEqual(DefaultValueExtractor.create_default_period(), 1)
        Teams(year=1985, period=1).save()
        self.assertEqual(DefaultValueExtractor.create_default_period(), 2)
        Teams(year=1985, period=2).save()
        self.assertEqual(DefaultValueExtractor.create_default_period(), 1)

    def test_create_default_prefecture(self):
        """
        Teamsにレコードが存在しない場合   -> 0(初期値)
        Teamsにレコードが存在している場合 -> 最新レコードのprefectureと同じ値を返す
        """
        self.assertEqual(DefaultValueExtractor.create_default_prefecture(), 0)
        Teams(prefecture=17).save()
        self.assertEqual(DefaultValueExtractor.create_default_prefecture(), 17)
        Teams(prefecture=1).save()
        self.assertEqual(DefaultValueExtractor.create_default_prefecture(), 1)

    def test_create_default_year_for_players(self):
        """
        Teamsにレコードが存在しない場合   -> 1939(初期値)
        Teamsにレコードが存在している場合 -> 最新レコードのyearと同じ値を返す
        """
        self.assertEqual(
            DefaultValueExtractor.create_default_year_for_players(), 1939)
        Teams(year=1985).save()
        self.assertEqual(
            DefaultValueExtractor.create_default_year_for_players(), 1985)
        Teams(year=2040).save()
        self.assertEqual(
            DefaultValueExtractor.create_default_year_for_players(), 2040)

    def test_create_default_team_id(self):
        """
        Teamsにレコードが存在しない場合   -> 1939(初期値)
        Teamsにレコードが存在している場合 -> 最新レコードのidと同じ値を返す
        """
        self.assertEqual(DefaultValueExtractor.create_default_team_id(), 0)
        Teams(year=1985, period=1).save()
        self.assertEqual(DefaultValueExtractor.create_default_team_id(), 1)
        Teams(year=1985, period=2).save()
        self.assertEqual(DefaultValueExtractor.create_default_team_id(), 2)

    def test_create_default_competition_type(self):
        """
        現在のチームに紐づくGamesのレコードが存在しない場合 -> 2(県大会)
        現在のそのチームに紐づくGamesのレコードが存在する場合
            最新が練習試合 -> 2(県大会)
            練習試合以外 -> 基本は同じ値を設定する
                例外:
                    夏 and 県大会 and 決勝 and 勝　であれば次は甲子園
                    秋 and 県大会 and ２回戦 and 勝　であれば次は地区大会
                    秋 and 地区大会 and ２回戦　であれば次はセンバツ
                妥協：
                    １回戦、３回戦がない場合は考慮しない
        """
        period = ChoicesFormatter.period_choices_to_dict()
        competition_choices = ChoicesFormatter.competition_choices_to_dict()
        round_choices = ChoicesFormatter.round_choices_to_dict()
        
        self.assertEqual(
            DefaultValueExtractor.create_default_competition_type(),
            competition_choices['県大会'])
        # 夏のチーム
        Teams(year=1985, period=period['夏']).save()

        self.assertEqual(
            DefaultValueExtractor.create_default_competition_type(),
            competition_choices['県大会'])

        t1 = Teams.objects.latest('pk')
        Games(
            team_id=t1,
            competition_type=competition_choices['練習試合'],
            competition_round=round_choices['練習試合']
        ).save()
        self.assertEqual(
            DefaultValueExtractor.create_default_competition_type(),
            competition_choices['県大会'])

        Games(
            team_id=t1,
            competition_type=competition_choices['県大会'],
            competition_round=round_choices['2回戦'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            DefaultValueExtractor.create_default_competition_type(),
            competition_choices['県大会'])

        Games(
            team_id=t1,
            competition_type=competition_choices['県大会'],
            competition_round=round_choices['2回戦'],
            score=0,
            run=1
        ).save()
        self.assertEqual(
            DefaultValueExtractor.create_default_competition_type(),
            competition_choices['県大会'])

        Games(
            team_id=t1,
            competition_type=competition_choices['県大会'],
            competition_round=round_choices['決勝'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            DefaultValueExtractor.create_default_competition_type(),
            competition_choices['甲子園'])

        Games(
            team_id=t1,
            competition_type=competition_choices['県大会'],
            competition_round=round_choices['決勝'],
            score=0,
            run=1
        ).save()
        self.assertEqual(
            DefaultValueExtractor.create_default_competition_type(),
            competition_choices['県大会'])

        # 秋のチーム
        Teams(year=1985, period=period['秋']).save()
        t2 = Teams.objects.latest('pk')
        self.assertEqual(
            DefaultValueExtractor.create_default_competition_type(),
            competition_choices['県大会'])

        Games(
            team_id=t2,
            competition_type=competition_choices['県大会'],
            competition_round=round_choices['2回戦'],
            score=0,
            run=1
        ).save()
        self.assertEqual(
            DefaultValueExtractor.create_default_competition_type(),
            competition_choices['県大会'])

        Games(
            team_id=t2,
            competition_type=competition_choices['県大会'],
            competition_round=round_choices['2回戦'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            DefaultValueExtractor.create_default_competition_type(),
            competition_choices['地区大会'])

        Games(
            team_id=t2,
            competition_type=competition_choices['地区大会'],
            competition_round=round_choices['2回戦'],
            score=0,
            run=1
        ).save()
        self.assertEqual(
            DefaultValueExtractor.create_default_competition_type(),
            competition_choices['地区大会'])

        Games(
            team_id=t2,
            competition_type=competition_choices['地区大会'],
            competition_round=round_choices['2回戦'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            DefaultValueExtractor.create_default_competition_type(),
            competition_choices['センバツ'])

        Games(
            team_id=t2,
            competition_type=competition_choices['センバツ'],
            competition_round=round_choices['2回戦'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            DefaultValueExtractor.create_default_competition_type(),
            competition_choices['センバツ'])

    def test_create_default_competition_round(self):
        """
        現在のチームに紐づくGamesのレコードが存在しない場合 -> 2(1回戦)
        現在のそのチームに紐づくGamesのレコードが存在する場合
            最新が練習試合 -> 2(1回戦)
            練習試合以外 -> 基本は前の試合で勝っていれば+1を設定する
                例外:
                    前の試合が負 であれば 2(1回戦)
                    前の試合が決勝 であれば次は2(1回戦)
                    秋 and 県大会 and ２回戦 and 勝　であれば次は2(1回戦)
                    秋 and 地区大会 and ２回戦　であれば次は2(1回戦)
                妥協：
                    １回戦、３回戦がない場合は考慮しない
        """
        period = ChoicesFormatter.period_choices_to_dict()
        competition_choices = ChoicesFormatter.competition_choices_to_dict()
        round_choices = ChoicesFormatter.round_choices_to_dict()
        
        self.assertEqual(
            DefaultValueExtractor.create_default_competition_round(),
            round_choices['1回戦'])
        # 夏のチーム
        Teams(year=1985, period=period['夏']).save()

        self.assertEqual(
            DefaultValueExtractor.create_default_competition_round(),
            round_choices['1回戦'])

        t1 = Teams.objects.latest('pk')
        Games(
            team_id=t1,
            competition_type=competition_choices['練習試合'],
            competition_round=round_choices['練習試合']
        ).save()
        self.assertEqual(
            DefaultValueExtractor.create_default_competition_round(),
            round_choices['1回戦'])

        Games(
            team_id=t1,
            competition_type=competition_choices['県大会'],
            competition_round=round_choices['2回戦'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            DefaultValueExtractor.create_default_competition_round(),
            round_choices['3回戦'])

        Games(
            team_id=t1,
            competition_type=competition_choices['県大会'],
            competition_round=round_choices['2回戦'],
            score=0,
            run=1
        ).save()
        self.assertEqual(
            DefaultValueExtractor.create_default_competition_round(),
            round_choices['1回戦'])

        Games(
            team_id=t1,
            competition_type=competition_choices['県大会'],
            competition_round=round_choices['決勝'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            DefaultValueExtractor.create_default_competition_round(),
            round_choices['1回戦'])

        Games(
            team_id=t1,
            competition_type=competition_choices['県大会'],
            competition_round=round_choices['決勝'],
            score=0,
            run=1
        ).save()
        self.assertEqual(
            DefaultValueExtractor.create_default_competition_round(),
            round_choices['1回戦'])

        # 秋のチーム
        Teams(year=1985, period=period['秋']).save()
        t2 = Teams.objects.latest('pk')
        self.assertEqual(
            DefaultValueExtractor.create_default_competition_round(),
            competition_choices['県大会'])

        Games(
            team_id=t2,
            competition_type=competition_choices['県大会'],
            competition_round=round_choices['2回戦'],
            score=0,
            run=1
        ).save()
        self.assertEqual(
            DefaultValueExtractor.create_default_competition_round(),
            round_choices['1回戦'])

        Games(
            team_id=t2,
            competition_type=competition_choices['県大会'],
            competition_round=round_choices['2回戦'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            DefaultValueExtractor.create_default_competition_round(),
            round_choices['1回戦'])

        Games(
            team_id=t2,
            competition_type=competition_choices['地区大会'],
            competition_round=round_choices['2回戦'],
            score=0,
            run=1
        ).save()
        self.assertEqual(
            DefaultValueExtractor.create_default_competition_round(),
            round_choices['1回戦'])

        Games(
            team_id=t2,
            competition_type=competition_choices['地区大会'],
            competition_round=round_choices['2回戦'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            DefaultValueExtractor.create_default_competition_round(),
            round_choices['1回戦'])

        Games(
            team_id=t2,
            competition_type=competition_choices['センバツ'],
            competition_round=round_choices['2回戦'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            DefaultValueExtractor.create_default_competition_round(),
            round_choices['3回戦'])

    def test_create_default_team_rank(self):
        """
        Gamesにレコードが存在しない場合   -> 0(初期値)
        Gamesにレコードが存在している場合 -> 最新レコードのrankと同じ値を返す
        """
        self.assertEqual(DefaultValueExtractor.create_default_team_rank(), 0)
        Teams(year=1985, period=1).save()
        t1 = Teams.objects.latest('pk')
        Games(team_id=t1, rank=1).save()
        self.assertEqual(DefaultValueExtractor.create_default_team_rank(), 1)
        Teams(year=1985, period=2).save()
        t2 = Teams.objects.latest('pk')
        Games(team_id=t2, rank=5).save()
        self.assertEqual(DefaultValueExtractor.create_default_team_rank(), 5)

    def test_select_display_players(self):
        """
        Teamsにレコードが存在しない場合
            -> 空の辞書を返す
        ModelSettingsのis_used_limit_choices_toがTrue
            -> 空の辞書を返す
        eamsにレコードが存在して、最新レコードが
            period == 1(夏)
                -> {"admission_year__gte": teams.year - 2,
                    "admission_year__lte": teams.year}
                   -> 3学年分表示させる
            period == 2(秋)
                -> {"admission_year__gte": teams.year - 1,
                    "admission_year__lte": teams.year}
                    -> 2学年分表示させる
        """
        self.assertEqual(DefaultValueExtractor.select_display_players(), {})
        Teams(year=1985, period=1).save()
        self.assertEqual(DefaultValueExtractor.select_display_players(), {
                         "admission_year__gte": 1983, "admission_year__lte": 1985})
        Teams(year=1985, period=2).save()
        self.assertEqual(DefaultValueExtractor.select_display_players(), {
                         "admission_year__gte": 1984, "admission_year__lte": 1985})
        ModelSettings(is_used_limit_choices_to=True).save()
        self.assertEqual(DefaultValueExtractor.select_display_players(), {})
        ModelSettings(is_used_limit_choices_to=False).save()
        self.assertEqual(DefaultValueExtractor.select_display_players(), {
                         "admission_year__gte": 1984, "admission_year__lte": 1985})

    def test_select_display_pitchers(self):
        """
        Teamsにレコードが存在しない場合
            -> 空の辞書を返す
        ModelSettingsのis_used_limit_choices_toがTrue
            -> 空の辞書を返す
        eamsにレコードが存在して、最新レコードが
            period == 1(夏)
                -> {"is_pitcher": True,
                    "admission_year__gte": teams.year - 2,
                    "admission_year__lte": teams.year}
                   -> 3学年分表示させる
            period == 2(秋)
                -> {"is_pitcher": True,
                    "admission_year__gte": teams.year - 1,
                    "admission_year__lte": teams.year}
                    -> 2学年分表示させる
        """
        self.assertEqual(
            DefaultValueExtractor.select_display_pitchers(), {
                "is_pitcher": True})
        Teams(year=1998, period=1).save()
        self.assertEqual(DefaultValueExtractor.select_display_pitchers(), {
                         "is_pitcher": True, "admission_year__gte": 1996, "admission_year__lte": 1998})
        Teams(year=1998, period=2).save()
        self.assertEqual(DefaultValueExtractor.select_display_pitchers(), {
                         "is_pitcher": True, "admission_year__gte": 1997, "admission_year__lte": 1998})
        ModelSettings(is_used_limit_choices_to=True).save()
        self.assertEqual(
            DefaultValueExtractor.select_display_pitchers(), {
                "is_pitcher": True})
        ModelSettings(is_used_limit_choices_to=False).save()
        self.assertEqual(DefaultValueExtractor.select_display_pitchers(), {
                         "is_pitcher": True, "admission_year__gte": 1997, "admission_year__lte": 1998})


class SavedValueExtractorTests(TestCase):
    def test_create_game_results(self):
        """
        score > run  -> 1(勝)
        score < run  -> 2(負)
        score == run -> 3(分)
        """
        self.assertEqual(
            SavedValueExtractor.create_game_results(
                self, 0, 0), 3)
        self.assertEqual(
            SavedValueExtractor.create_game_results(
                self, 10, 10), 3)
        self.assertEqual(
            SavedValueExtractor.create_game_results(
                self, 1, 0), 1)
        self.assertEqual(
            SavedValueExtractor.create_game_results(
                self, 8, 7), 1)
        self.assertEqual(
            SavedValueExtractor.create_game_results(
                self, 0, 1), 2)
        self.assertEqual(
            SavedValueExtractor.create_game_results(
                self, 3, 4), 2)

    def test_update_is_pitcher(self):
        """
        positionが1(投手) または is_pitchedがTrue（野手だけど登板した）の場合はTrue
        """
        self.assertTrue(SavedValueExtractor.update_is_pitcher(self, 1, True))
        self.assertTrue(SavedValueExtractor.update_is_pitcher(self, 1, False))
        self.assertTrue(SavedValueExtractor.update_is_pitcher(self, 2, True))
        self.assertFalse(SavedValueExtractor.update_is_pitcher(self, 2, False))

    def test_check_is_cold_game(self):
        """
        県大会決勝、甲子園の場合はis_cold_gameがTrueだった場合、Falseに修正して保存する
        """
        self.assertTrue(SavedValueExtractor.check_is_cold_game(self, True, 1, 1))
        self.assertFalse(SavedValueExtractor.check_is_cold_game(self, False, 1, 1))
        self.assertTrue(SavedValueExtractor.check_is_cold_game(self, True, 2, 2))
        self.assertFalse(SavedValueExtractor.check_is_cold_game(self, False, 2, 2))
        self.assertTrue(SavedValueExtractor.check_is_cold_game(self, True, 2, 6))
        self.assertFalse(SavedValueExtractor.check_is_cold_game(self, False, 2, 6))
        self.assertFalse(SavedValueExtractor.check_is_cold_game(self, True, 2, 7))
        self.assertFalse(SavedValueExtractor.check_is_cold_game(self, False, 2, 7))
        self.assertTrue(SavedValueExtractor.check_is_cold_game(self, True, 3, 1))
        self.assertFalse(SavedValueExtractor.check_is_cold_game(self, False, 3, 1))
        self.assertFalse(SavedValueExtractor.check_is_cold_game(self, True, 4, 1))
        self.assertFalse(SavedValueExtractor.check_is_cold_game(self, False, 4, 1))
        self.assertFalse(SavedValueExtractor.check_is_cold_game(self, True, 5, 1))
        self.assertFalse(SavedValueExtractor.check_is_cold_game(self, False, 5, 1))


class ChoicesFormatterTests(TestCase):
    def test_competition_choices_to_dict(self):
        self.assertEqual(
            ChoicesFormatter.competition_choices_to_dict(),
            {'選択': '', '練習試合': 1, '県大会': 2, '地区大会': 3, '甲子園': 4, 'センバツ': 5})

    def test_round_choices_to_dict(self):
        self.assertEqual(
            ChoicesFormatter.round_choices_to_dict(), {
                '選択': '', '練習試合': 1, '1回戦': 2, '2回戦': 3, '3回戦': 4, '準々決勝': 5, '準決勝': 6, '決勝': 7})

    def test_result_choices_to_dict(self):
        self.assertEqual(
            ChoicesFormatter.result_choices_to_dict(),
            {'選択': '', '勝': 1, '負': 2, '分': 3}
        )

    def test_rank_choices_to_dict(self):
        self.assertEqual(
            ChoicesFormatter.rank_choices_to_dict(), {
                '選択': '', '弱小': 1, 'そこそこ': 2, '中堅': 3, '強豪': 4, '名門': 5})

    def test_period_choices_to_dict(self):
        self.assertEqual(
            ChoicesFormatter.period_choices_to_dict(),
            {'選択': '', '夏': 1, '秋': 2}
        )

    def test_position_choices_to_dict(self):
        self.assertEqual(
            ChoicesFormatter.position_choices_to_dict(),
            {'選択': '', '投': 1, '捕': 2, '一': 3, '二': 4, '三': 5, '遊': 6, '外': 7}
        )
