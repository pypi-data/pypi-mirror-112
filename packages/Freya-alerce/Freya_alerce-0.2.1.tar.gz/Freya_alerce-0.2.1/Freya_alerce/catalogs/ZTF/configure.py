"""
configure.py is the most important file in Freya, this file is called for 
Freya’s core and FreyaAPI’s resources, is the only file you need to modify 
in principle. You need to complete the following methods. When using Freya’s 
method getData, you use this class for calls and depent what method call you 
need use ra and dec or hms, so that's why kwargs is used.
"""
import requests
import io
import numpy as np
from astropy.io import ascii

from Freya_alerce.catalogs.core.abstract_catalog import BaseCatalog
from Freya_alerce.core.utils import Utils

class ConfigureZTF(BaseCatalog):
    """
    Parameters:
    ------------
    ra : (float) 
        Right ascension
    dec :  (float) 
        Declination
    radius: (float) 
        Search radius
    nearest: (bool)
        True or False
    """
    def __init__(self,**kwagrs):
        self.ra = kwagrs.get('ra')
        self.dec = kwagrs.get('dec')
        self.radius = kwagrs.get('radius')
        self.nearest = kwagrs.get('nearest')

    def id_nearest (self,results):
        """ Get the idex of object id most closet to ra dec use a min angle
        """
        matrix = []
        for group in results.groups:
            matrix.append([group['ra'][0],group['dec'][0]])
        matrix = np.array(matrix)
        return_ = Utils().get_nearest(self.ra,self.dec,matrix)
        return return_ 
    
    def __split_filter(self,filter_):
        b = []
        for a_ in filter_:
            b.append(a_.split('z')[1])
        return b

    def get_matrix_data(self,result):
        ztfdic = ''
        result_ = ascii.read(result.text)
        if len(result_) <= 0:
            ztfdic = 'light curve not found' 
            return ztfdic

        #the most close object to radius
        if self.nearest is True:
            
            result_ = result_.group_by('oid')
            minztf = self.id_nearest(result_)
            ztf_matrix = np.array([result_.groups[minztf]['oid'],result_.groups[minztf]['ra'],
                                    result_.groups[minztf]['dec'],result_.groups[minztf]['mjd'],
                                    result_.groups[minztf]['mag'],result_.groups[minztf]['magerr'],
                                    self.__split_filter(result_.groups[minztf]['filtercode'])]).T
            return ztf_matrix
        # all objects in radius
        else:
            ztf_matrix = np.array([result_['oid'],result_['ra'],result_['dec'],result_['mjd'],
                                    result_['mag'],result_['magerr'],self.__split_filter(result_['filtercode'])]).T
            return ztf_matrix

    def zftcurves(self):
        """ Get light curves of ztf objects 
        Parameters
        ----------
        """
        baseurl="https://irsa.ipac.caltech.edu/cgi-bin/ZTF/nph_light_curves"
        data = {}
        data['POS']=f'CIRCLE {self.ra} {self.dec} {self.radius}'
        data['BANDNAME']='g,r,i'
        data['FORMAT'] = 'csv'
        result = requests.get(baseurl,params=data)
        ztfdic = ''
        #return result
        if result.status_code != 200: 
            ztfdic = result.status_code 
            return ztfdic
        else:
            return self.get_matrix_data(result)

    def get_lc(self):
        """
        Get all ligth curves data or the most close object,inside degree area from ZTF catalog.
        Return
        -------
        Return numpy array 2d with rows represent the objects and columns : ['obj','ra','dec','mjd','mag','magerr,'filter'].
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
        """
        data_return = self.zftcurves() 
        return data_return