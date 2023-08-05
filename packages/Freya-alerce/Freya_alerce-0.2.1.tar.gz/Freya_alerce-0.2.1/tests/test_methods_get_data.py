from unittest import TestCase, mock
from Freya_alerce.catalogs.core.data_lc import DataLcDegree,DataLcHms

class TestMethodsGetData(TestCase):
    
    def setUp(self):
        self.test_get_data_degree_all = DataLcDegree(catalog='test1',ra=139.33444972,dec=68.6350604,nearest=True)
        self.test_get_data_degree_one = DataLcDegree(catalog='test1',ra=139.33444972,dec=68.6350604,nearest=False)
        self.test_get_data_hms_all = DataLcHms(catalog='test2',hms = '9h17m20.26793280000689s +4h34m32.414496000003936s',nearest=True)
        self.test_get_data_hms_one = DataLcHms(catalog='test2',hms = '9h17m20.26793280000689s +4h34m32.414496000003936s',nearest=False)


    @mock.patch.object(DataLcDegree, "get_data")
    @mock.patch.object(DataLcHms, "get_data")
    def test(self,mock1,mock2):
        str_test = 'Ligth Curve Data'
        mock1.return_value = str_test
        mock2.return_value = str_test

        self.assertEqual(self.test_get_data_degree_all.get_data(), str_test)
        self.assertEqual(self.test_get_data_degree_one.get_data(), str_test)
        self.assertEqual(self.test_get_data_hms_all.get_data(), str_test)
        self.assertEqual(self.test_get_data_hms_one.get_data(), str_test)



        
if __name__ == '__main__':
    unittest.main() 

