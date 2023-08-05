import tempfile

from unittest import TestCase
from Freya_alerce.files.verify_file import Verify

class TestVerifyFiles(TestCase):
    

    def setUp(self):
        self.valid_source_api = 'api'
        self.valid_source_db = 'db'
        self.valid_source_other = 'other'
        self.valid_source_error_1 = 'cmd'
        self.valid_source_error_2 = 'web/HTPP'

    def test(self):
        self.assertTrue(Verify().verify_source(self.valid_source_api))
        self.assertTrue(Verify().verify_source(self.valid_source_db))
        self.assertTrue(Verify().verify_source(self.valid_source_other))
        self.assertFalse(Verify().verify_source(self.valid_source_error_1))
        self.assertFalse(Verify().verify_source(self.valid_source_error_2))

if __name__ == '__main__':
    unittest.main() 