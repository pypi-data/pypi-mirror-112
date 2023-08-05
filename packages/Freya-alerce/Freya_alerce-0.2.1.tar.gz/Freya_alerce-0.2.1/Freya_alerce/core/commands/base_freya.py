import os
import tempfile
import shutil
import zipfile #read zip files
import Freya_alerce.files # __path_
from Freya_alerce.files.verify_file import Verify
from Freya_alerce.files.list_file import ListFiles


class Base(object):
    """
    Base class to command line Freya, contains method for add new catalog inside Freya or in local folder, 
    created new local folder.

    Parameters
    --------------------------------------
    name : (string) 
        name with add catalog inside Freya or in local folder.
    source : (string) 
        origin source catalog [api,db]
    path : (string) 
        path where created catalogs.
    """

    def __init__(self,**kwargs):
        self.name = kwargs.get('name')
        if self.name:
            #self.name = self.name.replace(self.name[0],self.name[0].upper(),1)
            self.name = self.name.upper()
        self.new_name = kwargs.get('new_name')
        if self.new_name:
            self.new_name = self.new_name.upper()
        self.source = kwargs.get('source')
        self.path = kwargs.get('path')
    
    def create_module_catalog(self):
        """
        Create new catalog module inside Freya,
        first verify if source catalog is valid, 
        second verify the catalog already exist then get path
        for new module catalog and path template data,
        finaly try create the new module folder and extract the data.
        """
        
        #self.name= self.name.upper()
        if not Verify().verify_source(self.source):
            raise TypeError (f'The source not is valid')

        if Verify().verify_catalog_inside(self.name) or Verify().verify_catalog_local(self.name):  
            raise TypeError ('catalog already created')
        
        path_dir = self.path
        path_new_catalog = os.path.join(path_dir,self.name)
        path_tample_files_ = ListFiles().path_files__from_()     
        try: 
            with tempfile.TemporaryDirectory() as tmpdir:
                #print('created temporary directory', tmpdirname)
                extract_zip = zipfile.ZipFile(path_tample_files_)
                if self.source == 'api' or self.source == 'other':
                    list_names_files = ListFiles().files_api()
                elif self.source == 'db':
                    list_names_files = ListFiles().files_db()
                for file_ in list_names_files:
                    extract_zip.extract(file_, tmpdir)
                extract_zip.close()
                # Replace word 'NAME' from the name catalog
                if self.source == 'api' or self.source == 'other':
                    list_path = [os.path.join(tmpdir,f) for f in ListFiles().files_api()]
                    ListFiles().replace_in_files(list_path,'from Freya_alerce.catalogs.NAME import ConnectNAME','')
                elif self.source == 'db':
                    list_path = [os.path.join(tmpdir,f) for f in ListFiles().files_db()]
                ListFiles().replace_in_files(list_path,'NAME',self.name)
                shutil.copytree(tmpdir,path_new_catalog)
        except OSError as error:
            print(error)  
    
    def create_module_catalog_local(self):
        """
        Create new local catalog module ,
        first verify if source catalog is valid, 
        second verify the catalog already exist then get path
        for new module catalog and path template data,
        finaly try create the new module folder and extract the data.

        The catalog create in path with call the freya-admin.
        """
        path_new_catalog = os.path.join(self.path,f'Local{self.name}')
        path_tample_files_ = ListFiles().path_files__from_()     
        try: 
            with tempfile.TemporaryDirectory() as tmpdir:
                # create same of inside catalog
                self.path = tmpdir
                self.create_module_catalog()
                # extract setup
                extract_zip = zipfile.ZipFile(path_tample_files_)
                list_names_files = ListFiles().files_local()
                for file_ in list_names_files:
                    extract_zip.extract(file_, tmpdir)
                extract_zip.close()
                list_path_ = [os.path.join(tmpdir,'setup.py')]
                ListFiles().replace_in_files(list_path_,'NAME',self.name)
                shutil.copytree(tmpdir,path_new_catalog)
        except OSError as error:
            print(error)  

    def rename_catalog(self):
        """
        Rename catalog inside Freya
        """
        dir_catalogs = self.path
        try:
            #replace name catalog inside files
            path = os.path.join(dir_catalogs,self.name)
            list_path = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f))]
            list_path = [os.path.join(path,f) for f in list_path] # add 
            ListFiles().replace_in_files(list_path,self.name,self.new_name)
            #replace folder name
            path_ = path.split("/")
            path_[-1] = self.new_name
            path_ = "/".join(path_)
            os.rename(path, path_)
        except OSError as error:
            print(error)    
        
    def delete_catalog(self):
        """
        Delete catalog inside Freya
        """
        dir_catalogs = self.path
        try:
            path = os.path.join(dir_catalogs,self.name)
            shutil.rmtree(path)
        except OSError as error:
            print(error)