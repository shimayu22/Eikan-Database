from django.test import TestCase
from eikan.calculate_sabr import CalculateTeamSabr as cts


class CalculateTeamSabrTests(TestCase):
    def test_team_der(self):
        self.assertAlmostEqual(
            cts.team_der(self, 221, 38, 6, 22, 63, 0),
            0.7538, 3)
        self.assertAlmostEqual(
            cts.team_der(self, 221, 38, 6, 22, 63, 5),
            0.7153, 3)
        self.assertEqual(cts.team_der(self, 0, 0, 0, 0, 0, 0), 0)
