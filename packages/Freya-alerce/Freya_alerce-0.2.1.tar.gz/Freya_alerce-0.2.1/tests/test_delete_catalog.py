import tempfile
import os
from unittest import TestCase
from Freya_alerce.core.commands.base_freya import Base

class TestDeleteCatalog(TestCase):

    def setUp(self):
        self.tmp_test = tempfile.TemporaryDirectory()

    def test_delete_module_api(self):
        Base(name='test_api',source='api',path=self.tmp_test.name).create_module_catalog()
        path__module_api = os.path.join(self.tmp_test.name,'TEST_API')
        self.assertTrue(os.path.isdir(path__module_api))
        Base(name='test_api',path=self.tmp_test.name).delete_catalog()
        self.assertFalse(os.path.isdir(path__module_api))

    def test_delete_module_db(self):
        Base(name='test_db',source='db',path=self.tmp_test.name).create_module_catalog()
        path__module_db = os.path.join(self.tmp_test.name,'TEST_DB')
        self.assertTrue(os.path.isdir(path__module_db))
        Base(name='test_db',path=self.tmp_test.name).delete_catalog()
        self.assertFalse(os.path.isdir(path__module_db))

    def tearDown(self):
        self.tmp_test.cleanup()

if __name__ == '__main__':
    unittest.main() 