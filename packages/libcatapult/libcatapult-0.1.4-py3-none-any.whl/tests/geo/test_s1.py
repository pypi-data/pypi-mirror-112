import unittest
from datetime import datetime

from libcatapult.geo.s1 import S1Product, validate, common_polarisations


class TestS1Product(unittest.TestCase):

    def test_valid_name(self):
        result = S1Product("S1A_IW_GRDH_1SDV_20191130T173211_20191130T173240_030143_0371B4_E057")
        self.assertEqual(result.satellite, "S1A", "incorrect satellite")
        self.assertEqual(result.SAR_mode, "IW", "incorrect sar mode")
        self.assertEqual(result.product_type, "GRDH_1SDV", "incorrect product type")
        self.assertEqual(result.start_timestamp(), datetime.strptime("20191130T173211", "%Y%m%dT%H%M%S"), "incorrect start time")
        self.assertEqual(result.stop_timestamp(), datetime.strptime("20191130T173240", "%Y%m%dT%H%M%S"), "incorrect stop time")


class TestS1Validate(unittest.TestCase):

    def test_invalid_names(self):
        self.assertFalse(validate(""))
        self.assertFalse(validate("kjsfdagufhawlseqnxu32a\\wrhyuirygb no"))
        self.assertFalse(validate("            "))

    def test_valid_name(self):
        self.assertTrue(validate("S1A_IW_GRDH_1SDV_20191130T173211_20191130T173240_030143_0371B4_E057"))


class TestS1CommonPolarisations(unittest.TestCase):

    def test(self):
        input = [
            S1Product("S1A_IW_GRDH_1SDV_20191130T173211_20191130T173240_030143_0371B4_E057"),
            S1Product("S1A_IW_GRDH_1SSV_20191130T173211_20191130T173240_030143_0371B4_E057"),
        ]

        result = common_polarisations(input)
        self.assertListEqual(result, ['vv'])
