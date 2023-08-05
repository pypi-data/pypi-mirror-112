import importlib
import numpy as np

from Freya_alerce.files.verify_file import Verify
from Freya_alerce.core.utils import Utils
from Freya_alerce.catalogs.core.format_lc import FormatLC

"""
Class to get data from module catalog configured in Freya, first check if catalog exist inside Freya
and if not exist try import catalog from local folder. The data get is the all light curves of object in area. Use
degrees (ra,dec,radius) or  the format hh:mm:ss (hh:mm:ss,radius).
"""
class GetData(object):
    """
    Parameters
    -------------------------------------- 
    ra : (float) 
        (degrees) Right Ascension
    dec : (float) 
        (degrees) Declination 
    hms : (string)
        format ICRS
    radius : (float)
        Search radius
    format : (string)
        [numpy,csv,votable]
    catalog: (string)
        Catalog to search
    """

    def __init__(self,radius=0.0002777,format='numpy',nearest=False,**kwargs):
        self.catalog = kwargs.get('catalog').strip().upper()
        #self.catalog = self.catalog.replace(self.catalog[0],self.catalog[0].upper(),1)
        self.ra = kwargs.get('ra')
        self.dec = kwargs.get('dec')
        self.hms = kwargs.get('hms')
        self.radius = radius
        self.format = format
        self.nearest = nearest

        if self.format not in ['csv','votable']:
             return "inadmissible format in consult data"
    

    def generic_call_data(self,call_method):
        """
        Get the LC of catalog called in format CSV/VOTable. 
        Return
        -------
        Columns : ['obj','ra','dec','mjd','mag',''magerr,'filter','catalog'].
            obj : double
                Id of object in catalog
            ra : float
                Right ascension
            dec : float
                Declination
            mjd : float
                Julian day
            mag : float
                Magnitud
            magerr : float
                Magnitud error
            filter : str
                Band
            catalog : str
                Catalog source
        """
        # try :
        """
        Search catalog insiede Freya, if not exist search inside local folder.
        """
        if Verify().verify_catalog_inside(self.catalog):
            module = f'Freya_alerce.catalogs.{self.catalog}.configure'
        elif Verify().verify_catalog_local(self.catalog) :
                module = f'{self.catalog}.configure'

        # Import self.catalog
        mod = importlib.import_module(module)
        # Call class
        class_ =  getattr(mod,f'Configure{self.catalog}') 
        # Call method especific of class
        if call_method == 'get_lc_deg':
            method_ = class_(ra=self.ra,dec=self.dec,radius=self.radius,nearest=self.nearest).get_lc()      
        elif call_method == 'get_lc_hms':
            ra_,dec_ = Utils().hms_to_deg(self.hms)
            method_ = class_(ra=ra_,dec=dec_,radius=self.radius,nearest=self.nearest).get_lc()
        # add catalog source
        column_catalog = np.full(method_.shape[0],self.catalog)
        method_ = np.column_stack((method_, column_catalog))
        # set de estructure return with format
        if self.format == 'numpy':
            return FormatLC(method_).format_numpy()
        elif self.format == 'csv':
            return FormatLC(method_).format_csv()
        elif self.format == 'votable':
            return FormatLC(method_).format_votable()
        # except :
        #     print(f'No find the catalog : {self.catalog}')