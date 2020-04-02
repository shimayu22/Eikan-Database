from django.test import TestCase
from django.db import models
import eikan.models.games as g


class GamesTests(TestCase):
    def test_set_game_results(self):
        self.assertEqual(g.set_game_results(0, 0), 3)
        self.assertEqual(g.set_game_results(10, 10), 3)
        self.assertEqual(g.set_game_results(1, 0), 1)
        self.assertEqual(g.set_game_results(8, 7), 1)
        self.assertEqual(g.set_game_results(0, 1), 2)
        self.assertEqual(g.set_game_results(3, 4), 2)
