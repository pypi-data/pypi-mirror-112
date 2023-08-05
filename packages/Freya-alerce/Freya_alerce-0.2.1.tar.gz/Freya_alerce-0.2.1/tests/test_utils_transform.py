import tempfile

from unittest import TestCase
from Freya_alerce.core.utils import Utils

class TestUtilsTransform(TestCase):

    def setUp(self):
        self.test_ra = 139.33444972
        self.test_dec = 68.6350604
        self.test_hms = '09h17m20.26793280000689s +68d38m06.2174s'#+4h34m32.414496000003936s'
        self.test_mag = 14.033394136845427
        self.test_magerr = 0.0012384787365595684

    def test(self):
        #print(Utils().deg_to_hms(self.test_ra,self.test_dec))
        #print(Utils().hms_to_deg(self.test_hms))
        #self.assertEqual(self.test_hms, Utils().deg_to_hms(self.test_ra,self.test_dec))
        self.assertAlmostEqual(self.test_ra, Utils().hms_to_deg(self.test_hms)[0])
        self.assertAlmostEqual(self.test_dec, Utils().hms_to_deg(self.test_hms)[1])
        self.assertEqual(self.test_mag,Utils().flux_to_mag(0.008843869902193546))
        self.assertEqual(self.test_magerr,Utils().fluxerr_to_magerr(1.0087999726238195e-05,0.008843869902193546))
        

if __name__ == '__main__':
    unittest.main() 