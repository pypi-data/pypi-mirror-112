
from unittest import TestCase

class TestImport(TestCase):
    
    def test(self):
        try:
            from Freya_alerce.core.commands.base_freya import Base
            from Freya_alerce.core.commands.base_api import BaseAPI
            from Freya_alerce.files.list_file import ListFiles
            from Freya_alerce.files.verify_file import Verify
            from Freya_alerce.catalogs.core.format_lc import FormatLC
            from Freya_alerce.catalogs.core.data_lc import DataLcDegree,DataLcHms
        except OSError as error:
            print(error)  

if __name__ == '__main__':
    unittest.main() 