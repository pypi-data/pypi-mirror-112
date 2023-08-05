import tempfile
import os
from unittest import TestCase
from Freya_alerce.core.commands.base_freya import Base
from Freya_alerce.files.list_file import ListFiles

class TestRenameCatalog(TestCase):

    def setUp(self):
        self.tmp_test = tempfile.TemporaryDirectory()

    def test_rename_api(self):
        Base(name='test',source='api',path=self.tmp_test.name).create_module_catalog()
        path__module = os.path.join(self.tmp_test.name,'TEST')
        self.assertTrue(os.path.isdir(path__module))
        Base(name='test',new_name='test2',path=self.tmp_test.name).rename_catalog()
        path__module = os.path.join(self.tmp_test.name,'TEST2')
        self.assertTrue(os.path.isdir(path__module))

    def test_rename_api(self):
        Base(name='test3',source='db',path=self.tmp_test.name).create_module_catalog()
        path__module = os.path.join(self.tmp_test.name,'TEST3')
        self.assertTrue(os.path.isdir(path__module))
        Base(name='test3',new_name='test4',path=self.tmp_test.name).rename_catalog()
        path__module = os.path.join(self.tmp_test.name,'TEST4')
        self.assertTrue(os.path.isdir(path__module))

    def tearDown(self):
        self.tmp_test.cleanup()

if __name__ == '__main__':
    unittest.main() 