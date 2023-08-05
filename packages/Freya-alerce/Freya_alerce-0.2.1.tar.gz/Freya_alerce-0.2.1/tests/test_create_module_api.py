import tempfile
import os
from unittest import TestCase
from Freya_alerce.core.commands.base_freya import Base

class TestCreateModule(TestCase):
    
    def setUp(self):
        self.tmp_test = tempfile.TemporaryDirectory()

    def test_module_api(self):
        Base(name='test_api',source='api',path=self.tmp_test.name).create_module_catalog()
        path__module_api = os.path.join(self.tmp_test.name,'TEST_API')
        self.assertTrue(os.path.isdir(path__module_api))

    def test_module_db(self):
        Base(name='test_db',source='db',path=self.tmp_test.name).create_module_catalog()
        path__module_db = os.path.join(self.tmp_test.name,'TEST_DB')
        self.assertTrue(os.path.isdir(path__module_db))

    def test_module_other(self):
        Base(name='test_other',source='other',path=self.tmp_test.name).create_module_catalog()
        path__module_other = os.path.join(self.tmp_test.name,'TEST_OTHER')
        self.assertTrue(os.path.isdir(path__module_other))

    def tearDown(self):
        self.tmp_test.cleanup()

if __name__ == '__main__':
    unittest.main() 