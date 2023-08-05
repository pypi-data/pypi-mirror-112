import os
import sys
import subprocess
import tempfile
import shutil
import zipfile #read zip files
import Freya_alerce.files # __path__
from git import Repo
from Freya_alerce.files.verify_file import Verify
from Freya_alerce.files.list_file import ListFiles

class BaseAPI(object):
    """
    Base class to command line Freya for new api (FreyaAPI) and add resources in FreyaAPI.

    Parameters
    --------------------------------------
    name : (string) 
        name catalog inside Freya with add resource in FreyaAPI
    path : (string) 
        path where created FreyaAPI, local folder for catalogs and
        add resources in FreyaAPI.
    """

    def __init__(self,**kwargs):
        self.name = kwargs.get('name')
        if self.name:
            #self.name = self.name.replace(self.name[0],self.name[0].upper(),1)
            self.name = self.name.upper()
        self.path = kwargs.get('path')    
    
    
    def create_new_api(self):
        """
        Create a new FreyaAPI, the new api created in path
        with call the freya-admin --newapi
        """
        # Path create new api
        path_new_api =  os.path.join(self.path,'FreyaAPI')
        try: 
            tmpdir = tempfile.TemporaryDirectory() # path temp
            Repo.clone_from("https://github.com/fernandezeric/FreyaAPI", tmpdir.name)
            path_temp = os.path.join(tmpdir.name,'FreyaAPI')
            subprocess.check_call([sys.executable, '-m','pip', 'install','-r',os.path.join(path_temp,'requirements.txt')])
            shutil.copytree(path_temp,path_new_api)
            tmpdir.cleanup()
        except OSError as error:
            print(error)    
    
    def create_new_resource(self):
        """
        Add resource to FreyaAPI, first verify the catalog exist inside Freya 
        or in the local catalogs folder.
        """
        # Verify 
        if not Verify().verify_catalog_inside(self.name) and not Verify().verify_catalog_local(self.name):
            raise TypeError ('First created catalog inside Freya or local ')
        
        # Get path to template files
        path_template_resource = ListFiles().path_files_resource() # Path resource
        path_api = self.path
        if path_api.split('/')[-1] != 'FreyaAPI':
            raise TypeError ('Needs to be on the root path of FreyaAPI')
        else:
            path_new_resource = os.path.join(path_api,f'app/main/resources_freya/{self.name}_resource')

        try: 
            with tempfile.TemporaryDirectory() as tmpdir:
                extract_zip = zipfile.ZipFile(path_template_resource)
                extract_zip.extractall(tmpdir)
                extract_zip.close()
                list_path = [os.path.join(tmpdir,'resource.py')]
                ListFiles().replace_in_files(list_path,'NAME',self.name)
                shutil.copytree(tmpdir,path_new_resource)
        except OSError as error:
            print(error)    