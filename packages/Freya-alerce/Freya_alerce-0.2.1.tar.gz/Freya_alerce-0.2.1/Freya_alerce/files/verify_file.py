
import Freya_alerce.catalogs # __path__ # dir modules
import os
import importlib

class Verify(object):

    def verify_catalog_inside(self,name):
        """
        Verify name catalog already exist inside Freya.
        Parameters
        ----------
        name : string
            Name to search.
        Return: bool
        ----------
        Return True if catalog exists inside Freya in other case
        return False.
        """
        self.name = name
        dir_catalogs = Freya_alerce.catalogs.__path__[0]
        if self.name  in os.listdir(dir_catalogs) :
             return True 
        return False

    def verify_catalog_local(self,name):
        """
        Verify if catalogue path exist who a package in PYTHONPATH.
        Parameters
        ----------
        name : string
            Name to search.
        Return: bool
        ----------
        Return True if catalog exists in other case
        return False.
        """
        self.name = name
        try:
            mod = importlib.import_module(f'{self.name}')
            return True
        except:
            return False
    
    def verify_source(self,source):
        """
        Verify if source of catalog is permitted who source.
        Parameters
        ----------
        source : string
            valid source [api,db,other]
        Return: bool
        ----------
        Return True if source is valid.
        """
        self.source = source
        if self.source in ['api','db','other']:
            return True
        return False
