from django.test import TestCase
from eikan.models import Teams, Players, Games, FielderResults, FielderTotalResults, PitcherResults, PitcherTotalResults, TeamTotalResults
from eikan.model_manager import ChoicesFormatter


class TeamsTests(TestCase):
    def test_unique_key_check(self):
        """(year, period)"""
        period = ChoicesFormatter.period_choices_to_dict()
        Teams(year=1985, period=period['夏']).save()
        Teams(year=1985, period=period['秋']).save()
        self.assertEqual(Teams.objects.count(), 2)
        with self.assertRaises(Exception):
            Teams(year=1985, period=period['夏']).save()


class PlayersTests(TestCase):
    def test_unique_key_check(self):
        """(addmission_year, name)"""
        Players(admission_year=1985, name="桑田").save()
        Players(admission_year=1985, name="清原").save()
        self.assertEqual(Players.objects.count(), 2)
        with self.assertRaises(Exception):
            Players(admission_year=1985, name="桑田").save()


class FielderResultsTests(TestCase):
    def test_unique_key_check(self):
        """(game_id, player_id)"""
        period = ChoicesFormatter.period_choices_to_dict()
        competition_choices = ChoicesFormatter.competition_choices_to_dict()
        round_choices = ChoicesFormatter.round_choices_to_dict()
        # データセット
        Teams(year=1985, period=period['夏']).save()
        t1 = Teams.objects.latest('pk')
        Players(admission_year=1985, name="桑田", position="1").save()
        Players(admission_year=1985, name="清原", position="3").save()
        Games(team_id=t1,
              competition_type=competition_choices['県大会'],
              competition_round=round_choices['1回戦'],
              score=1,
              run=0).save()
        g1 = Games.objects.latest('pk')
        p1 = Players.objects.get(name="桑田")
        p2 = Players.objects.get(name="清原")
        FielderResults(game_id=g1, player_id=p1).save()
        FielderResults(game_id=g1, player_id=p2).save()
        self.assertEqual(FielderResults.objects.count(), 2)
        with self.assertRaises(Exception):
            FielderResults(game_id=g1, player_id=p2).save()


class PitcherResultsTests(TestCase):
    def test_unique_key_check(self):
        """(game_id, player_id)"""
        period = ChoicesFormatter.period_choices_to_dict()
        competition_choices = ChoicesFormatter.competition_choices_to_dict()
        round_choices = ChoicesFormatter.round_choices_to_dict()
        # データセット
        Teams(year=1985, period=period['夏']).save()
        t1 = Teams.objects.latest('pk')
        Players(admission_year=1985, name="桑田", position=1).save()
        Players(admission_year=1985, name="清原", position=1).save()
        Games(team_id=t1,
              competition_type=competition_choices['県大会'],
              competition_round=round_choices['1回戦'],
              score=1,
              run=0).save()
        g1 = Games.objects.latest('pk')
        p1 = Players.objects.get(name="桑田")
        p2 = Players.objects.get(name="清原")
        PitcherResults(game_id=g1, player_id=p1).save()
        PitcherResults(game_id=g1, player_id=p2).save()
        self.assertEqual(PitcherResults.objects.count(), 2)
        with self.assertRaises(Exception):
            PitcherResults(game_id=g1, player_id=p1).save()


class FielderTotalResultsTests(TestCase):
    def test_unique_key_check(self):
        """player_id"""
        Players(admission_year=1985, name="桑田").save()
        Players(admission_year=1985, name="清原").save()
        p1 = Players.objects.get(name="清原")
        with self.assertRaises(Exception):
            FielderTotalResults(player=p1).save()


class PitcherTotalResultsTests(TestCase):
    def test_unique_key_check(self):
        """player_id"""
        # データセット
        Players(admission_year=1985, name="桑田", position=1).save()
        Players(admission_year=1985, name="清原", position=1).save()
        p1 = Players.objects.get(name="桑田")
        with self.assertRaises(Exception):
            PitcherTotalResults(player=p1).save()


class TeamsTotalResultsTests(TestCase):
    def test_unique_key_check(self):
        """team_id"""
        period = ChoicesFormatter.period_choices_to_dict()
        Teams(year=1985, period=period['夏']).save()
        Teams(year=1985, period=period['秋']).save()
        t1 = Teams.objects.get(year=1985, period=period['夏'])
        with self.assertRaises(Exception):
            TeamTotalResults(team=t1).save()
