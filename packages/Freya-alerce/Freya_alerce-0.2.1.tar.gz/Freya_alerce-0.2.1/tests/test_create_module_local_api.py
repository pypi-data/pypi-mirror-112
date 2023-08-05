import tempfile
import os
from unittest import TestCase
from Freya_alerce.core.commands.base_freya import Base

class TestCreateModuleLocal(TestCase):
    

    def setUp(self):
        self.tmp_test = tempfile.TemporaryDirectory()

    def test_module_api_local(self):
        Base(name='test_api',source='api',path=self.tmp_test.name).create_module_catalog_local()
        path__module_api_local = os.path.join(self.tmp_test.name,'LocalTEST_API')
        self.assertTrue(os.path.isdir(path__module_api_local))

    def test_module_db_local(self):
        Base(name='test_db',source='db',path=self.tmp_test.name).create_module_catalog_local()
        path__module_db_local = os.path.join(self.tmp_test.name,'LocalTEST_DB')
        self.assertTrue(os.path.isdir(path__module_db_local))

    def test_module_other_local(self):
        Base(name='test_other',source='other',path=self.tmp_test.name).create_module_catalog_local()
        path__module_other_local = os.path.join(self.tmp_test.name,'LocalTEST_OTHER')
        self.assertTrue(os.path.isdir(path__module_other_local))
    
    def tearDown(self):
        self.tmp_test.cleanup()

if __name__ == '__main__':
    unittest.main() 