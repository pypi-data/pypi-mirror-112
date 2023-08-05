import tempfile
import os
import Freya_alerce.files # __path__

from unittest import TestCase
from Freya_alerce.files.list_file import ListFiles

class TestListFiles(TestCase):
    

    def setUp(self):
        self.return_files_api = ['configure.py','__init__.py']
        self.return_files_db = ['configure.py','connect.py','__init__.py']
        self.return_files_local = ['setup.py','requirements.txt']
        self.return_path_files_from = os.path.join(Freya_alerce.files.__path__[0],'file_templates','from_.zip')
        self.return_path_files_resource = os.path.join(Freya_alerce.files.__path__[0],'file_templates','newresource.zip')
        

    def test(self):
        self.assertEqual(ListFiles().files_api(), self.return_files_api)
        self.assertEqual(ListFiles().files_db(), self.return_files_db)
        self.assertEqual(ListFiles().files_local(), self.return_files_local)
        self.assertEqual(ListFiles().path_files__from_(), self.return_path_files_from)
        self.assertEqual(ListFiles().path_files_resource(), self.return_path_files_resource)
        
if __name__ == '__main__':
    unittest.main() 