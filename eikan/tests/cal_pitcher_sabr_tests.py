from django.test import TestCase
from eikan.calculate_sabr import CalculatePitcherSabr as cps


class CalculatePitcherSabrTests(TestCase):

    def test_innings_conversion_for_display(self):
        self.assertEqual(cps.innings_conversion_for_display(50, 0), 50.0)
        self.assertEqual(cps.innings_conversion_for_display(10, 1), 10.1)
        self.assertEqual(cps.innings_conversion_for_display(0, 10), 3.1)
        self.assertEqual(cps.innings_conversion_for_display(0, 9), 3.0)
        self.assertEqual(cps.innings_conversion_for_display(5, 6), 7.0)
        self.assertEqual(cps.innings_conversion_for_display(5, 7), 7.1)

    def test_innings_conversion_for_calculate(self):
        self.assertEqual(
            cps.innings_conversion_for_calculate(
                10, 0), 30.0)
        self.assertEqual(
            cps.innings_conversion_for_calculate(
                178, 2), 536.0)
        self.assertEqual(
            cps.innings_conversion_for_calculate(
                10, 6), 36.0)
        self.assertEqual(
            cps.innings_conversion_for_calculate(
                10, 7), 37.0)

    def test_earned_runs_average(self):
        self.assertAlmostEqual(
            cps.earned_runs_average(
                536.0, 79), 3.979, 3)
        self.assertEqual(cps.earned_runs_average(0, 0), 0)
        self.assertEqual(cps.earned_runs_average(0, 3), 0)

    def test_runs_average(self):
        self.assertAlmostEqual(
            cps.runs_average(
                536.0, 82), 4.131, 3)
        self.assertEqual(cps.runs_average(0, 0), 0)
        self.assertEqual(cps.runs_average(0, 3), 0)

    def test_walks_plus_hits_per_inning_pitched(self):
        self.assertAlmostEqual(
            cps.walks_plus_hits_per_inning_pitched(
                536.0, 140, 56), 1.097, 3)
        self.assertEqual(
            cps.walks_plus_hits_per_inning_pitched(
                0, 0, 0), 0)
        self.assertEqual(
            cps.walks_plus_hits_per_inning_pitched(
                0, 1, 1), 0)

    def test_strike_out_per_bbhp(self):
        self.assertAlmostEqual(
            cps.strike_out_per_bbhp(
                56, 229), 4.09, 2)
        self.assertEqual(
            cps.strike_out_per_bbhp(
                1, 0), 0)
        self.assertEqual(
            cps.strike_out_per_bbhp(
                0, 1), 0)

    def test_strike_out_per_game(self):
        self.assertAlmostEqual(
            cps.strike_out_per_game(
                536.0, 229), 11.54, 2)
        self.assertEqual(
            cps.strike_out_per_bbhp(
                1, 0), 0)
        self.assertEqual(
            cps.strike_out_per_bbhp(
                0, 1), 0)

    def test_strike_out_percentage(self):
        self.assertAlmostEqual(
            cps.strike_out_percentage(
                731, 229), 0.31, 2)
        self.assertEqual(
            cps.strike_out_percentage(
                1, 0), 0)
        self.assertEqual(
            cps.strike_out_percentage(
                0, 1), 0)

    def test_bbhp_per_game(self):
        self.assertAlmostEqual(
            cps.bbhp_per_game(536.0, 56), 2.82, 2)
        self.assertEqual(
            cps.bbhp_per_game(
                1, 0), 0)
        self.assertEqual(
            cps.bbhp_per_game(
                0, 1), 0)

    def test_bbhp_percentage(self):
        self.assertAlmostEqual(cps.bbhp_percentage(731, 56), 0.0766, 3)
        self.assertEqual(
            cps.bbhp_percentage(
                1, 0), 0)
        self.assertEqual(
            cps.bbhp_percentage(
                0, 1), 0)

    def test_home_run_per_game(self):
        self.assertAlmostEqual(
            cps.home_run_per_game(
                536.0, 33), 1.66, 2)
        self.assertEqual(
            cps.home_run_per_game(
                1, 0), 0)
        self.assertEqual(
            cps.home_run_per_game(
                0, 1), 0)

    def test_home_run_percentage(self):
        self.assertAlmostEqual(
            cps.home_run_percentage(
                731, 33), 0.0451, 2)
        self.assertEqual(
            cps.home_run_percentage(
                1, 0), 0)
        self.assertEqual(
            cps.home_run_percentage(
                0, 1), 0)

    def test_left_on_base_percentage(self):
        self.assertAlmostEqual(
            cps.left_on_base_percentage(140, 67, 33, 82), 0.777, 2
        )
        self.assertEqual(
            cps.left_on_base_percentage(
                1, 0, 1, 1), 0.0)
        self.assertEqual(
            cps.left_on_base_percentage(
                0, 1, 0, 0), 1.0)
        self.assertAlmostEqual(
            cps.left_on_base_percentage(0, 0, 0, 0), 0.0)

    def test_pitch_per_inning(self):
        self.assertAlmostEqual(
            cps.pitch_per_inning(536.0, 2848), 15.940, 2
        )

    def test_hit_per_game(self):
        self.assertAlmostEqual(
            cps.hit_per_game(536.0, 140), 7.052, 2
        )
        self.assertEqual(
            cps.hit_per_game(0, 140), 0.0
        )

    def test_hit_percentage(self):
        self.assertAlmostEqual(
            cps.hit_percentage(731, 140), 0.1915, 3
        )
        self.assertEqual(
            cps.hit_percentage(0, 140), 0.0
        )
