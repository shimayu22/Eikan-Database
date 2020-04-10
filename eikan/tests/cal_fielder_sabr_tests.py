from django.test import TestCase
from eikan.calculate_sabr import CalculateFielderSabr as cfs


class CalculateFielderSabrTests(TestCase):
    def test_total_bases(self):
        self.assertEqual(cfs.total_bases(110, 20, 5, 18), 194)
        self.assertEqual(cfs.total_bases(0, 0, 0, 0), 0)

    def test_slugging_percentage(self):
        self.assertAlmostEqual(
            cfs.slugging_percentage(384, 194), 0.505, 3)
        self.assertEqual(cfs.slugging_percentage(0, 1), 0)
        self.assertEqual(cfs.slugging_percentage(1, 0), 0)

    def test_on_base_percentage(self):
        self.assertAlmostEqual(
            cfs.on_base_percentage(384, 36, 110), 0.3476, 3
        )
        self.assertEqual(cfs.on_base_percentage(0, 0, 0), 0)
        self.assertEqual(cfs.on_base_percentage(0, 1, 0), 1)

    def test_on_base_plus_slugging(self):
        self.assertAlmostEqual(
            cfs.on_base_plus_slugging(0.343, 0.505), 0.848, 3)

    def test_batting_runs(self):
        self.assertAlmostEqual(
            cfs.batting_runs(110, 20, 5, 18, 33, 384), 16.9299, 3
        )

    def test_weighted_on_base_average(self):
        self.assertAlmostEqual(
            cfs.weighted_on_base_average(
                110, 20, 5, 18, 33, 384), 0.3678, 3)
        self.assertEqual(
            cfs.weighted_on_base_average(0, 0, 0, 0, 0, 0), 0)
        self.assertEqual(
            cfs.weighted_on_base_average(0, 0, 0, 0, 0, 1), 0)

    def test_gross_production_average(self):
        self.assertAlmostEqual(
            cfs.gross_production_average(0.343, 0.505), 0.2806, 3)
        self.assertEqual(cfs.gross_production_average(0, 0), 0)

    def test_batting_average(self):
        self.assertAlmostEqual(
            cfs.batting_average(384, 110), 0.286, 3
        )
        self.assertEqual(cfs.batting_average(0, 1), 0)
        self.assertEqual(cfs.batting_average(1, 0), 0)

    def test_bb_hp_percentage(self):
        self.assertAlmostEqual(
            cfs.bb_hp_percentage(384, 33, 0), 0.079136, 3
        )
        self.assertEqual(cfs.bb_hp_percentage(0, 1, 0), 1)
        self.assertEqual(cfs.bb_hp_percentage(0, 0, 0), 0)
        self.assertEqual(cfs.bb_hp_percentage(1, 0, 0), 0)

    def test_isolated_discipline(self):
        self.assertAlmostEqual(
            cfs.isolated_discipline(0.343, 0.286), 0.05700, 3
        )

    def test_isolated_power(self):
        self.assertAlmostEqual(
            cfs.isolated_power(0.505, 0.286), 0.219000, 3
        )

    def test_bb_hbp_per_so(self):
        self.assertAlmostEqual(
            cfs.bb_hbp_per_so(110, 33), 0.3000, 3
        )
        self.assertEqual(cfs.bb_hbp_per_so(1, 0), 0)
        self.assertEqual(cfs.bb_hbp_per_so(0, 1), 0)

    def test_power_speed_number(self):
        self.assertAlmostEqual(
            cfs.power_speed_number(18, 12), 14.4000, 2
        )
        self.assertEqual(cfs.power_speed_number(0, 0), 0)
        self.assertEqual(cfs.power_speed_number(1, 0), 0)
        self.assertEqual(cfs.power_speed_number(0, 1), 0)
