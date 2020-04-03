from django.test import TestCase
from django.db import models
from eikan.models import Teams
from eikan.model_manager import DefaultValueExtractor, SavedValueExtractor


class DefaultValueExtractorTests(TestCase):
    def test_create_default_year_for_teams(self):
        """
        Teamsにレコードが存在しない場合 -> 1941(初期値)
        Teamsにレコードが存在して、
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
