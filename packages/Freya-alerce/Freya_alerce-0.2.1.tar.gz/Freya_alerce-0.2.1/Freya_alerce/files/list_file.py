import fileinput #replace into files
import os

from Freya_alerce.files.file_templates.path_file_templates import basedir_tf

class ListFiles(object):



    def replace_in_files(self,paths,raplace_word,word):
        """
        Replace a 'word' for 'new word' in specific file.
        Parameters
        ----------
        paths: list
            List of paths of file what replece string.
        relace_word: string
            Original string in file.
        word: string
            New string to replace.
        Return
        ----------

        """
        self.list_path = paths
        self.replace_word = raplace_word
        self.word = word
        for file in self.list_path:
            with fileinput.FileInput(f'{file}', inplace=True) as file_:
                for line in file_:
                    print(line.replace(f'{self.replace_word}', f'{self.word}'), end='')
    
    def files_api(self):
        """
        Get names files use in api.
        Parameters
        ----------
        Return
        ----------
        Return list with name files necessary to extract for api source.
        """
        return ['configure.py','__init__.py']

    def files_db(self):
        """
        Get names files use in data base.
        Parameters
        ----------
        Return
        ----------
        Return list with name files necessary to extract for data base source.
        """
        return ['configure.py','connect.py','__init__.py']

    def files_local(self):
        """
        Get names files use in local catalog.
        Parameters
        ----------
        Return
        ----------
        Return list with name files necessary to extract in local module-catalog.
        """
        return ['setup.py','requirements.txt']

    def path_files__from_(self):
        """
        Get path templeta file from db/api.
        Parameters
        ----------
        Return
        ----------
        Return path of file template for new module-catalog.
        """
        return os.path.join(basedir_tf,'from_.zip')

    def path_files_resource(self):
        """
        Get the path resource generic.
        Parameters
        ----------
        Return
        ----------
        Return path of file template for new resource of and api.
        """
        return os.path.join(basedir_tf,'newresource.zip')