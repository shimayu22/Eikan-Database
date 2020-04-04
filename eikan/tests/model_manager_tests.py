from django.test import TestCase
from eikan.models import Teams, Games, ModelSettings
from eikan.model_manager import DefaultValueExtractor, SavedValueExtractor


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
        self.assertEqual(DefaultValueExtractor.create_default_year_for_players(), 1939)
        Teams(year=1985).save()
        self.assertEqual(DefaultValueExtractor.create_default_year_for_players(), 1985)
        Teams(year=2040).save()
        self.assertEqual(DefaultValueExtractor.create_default_year_for_players(), 2040)
    
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
        self.assertEqual(DefaultValueExtractor.select_display_players(), {"admission_year__gte": 1983, "admission_year__lte": 1985})
        Teams(year=1985, period=2).save()
        self.assertEqual(DefaultValueExtractor.select_display_players(), {"admission_year__gte": 1984, "admission_year__lte": 1985})
        ModelSettings(is_used_limit_choices_to=True).save()
        self.assertEqual(DefaultValueExtractor.select_display_players(), {})
        ModelSettings(is_used_limit_choices_to=False).save()
        self.assertEqual(DefaultValueExtractor.select_display_players(), {"admission_year__gte": 1984, "admission_year__lte": 1985})

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
        self.assertEqual(DefaultValueExtractor.select_display_pitchers(), {"is_pitcher": True})
        Teams(year=1998, period=1).save()
        self.assertEqual(DefaultValueExtractor.select_display_pitchers(), {"is_pitcher": True, "admission_year__gte": 1996, "admission_year__lte": 1998})
        Teams(year=1998, period=2).save()
        self.assertEqual(DefaultValueExtractor.select_display_pitchers(), {"is_pitcher": True, "admission_year__gte": 1997, "admission_year__lte": 1998})
        ModelSettings(is_used_limit_choices_to=True).save()
        self.assertEqual(DefaultValueExtractor.select_display_pitchers(), {"is_pitcher": True})
        ModelSettings(is_used_limit_choices_to=False).save()
        self.assertEqual(DefaultValueExtractor.select_display_pitchers(), {"is_pitcher": True, "admission_year__gte": 1997, "admission_year__lte": 1998})


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
