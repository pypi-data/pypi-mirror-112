
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
from astropy.coordinates import SkyCoord
from astropy import units as u

from Freya_alerce.catalogs.core.abstract_catalog import BaseCatalog
from Freya_alerce.core.utils import Utils

class ConfigurePS1(BaseCatalog):
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
    def __init__(self,*args,**kwagrs):
        self.ra = kwagrs.get('ra')
        self.dec = kwagrs.get('dec')
        self.radius = kwagrs.get('radius')
        self.nearest = kwagrs.get('nearest')

    def ps1cone(self, format='csv',baseurl="https://catalogs.mast.stsci.edu/api/v0.1/panstarrs", **kw):
            #table="mean",release="dr1",format="csv",columns=None,
        """Do a cone search of the PS1 catalog
        Parameters
        ----------
        """
        data = kw.copy()
        data['ra'] = self.ra
        data['dec'] = self.dec
        data['radius'] = self.radius
        return self.ps1search(format=format,baseurl=baseurl, **data)

    def ps1search(self,format='csv',table="mean",release="dr1",columns=None,baseurl="https://catalogs.mast.stsci.edu/api/v0.1/panstarrs",**kw):
        """Do a general search of the PS1 catalog (possibly without ra/dec/radius)
        
        Parameters
        ----------
        """
        data = kw.copy()
        url = f"{baseurl}/{release}/{table}.{format}"
        data['columns'] = '[{}]'.format(','.join(columns))
        r = requests.get(url, params=data)
        r.raise_for_status()
        # if self.format == "json":
        #     return r.json()
        return r.text

    def ps1ids(self):
        """Get ids (ps1 id) of objects in a radius with respect to ra and dec
        Parameters
        ----------
        """
        constraints = {'nDetections.gt':1}
        columns = ['objID','raMean','decMean']
        results = self.ps1cone(release='dr2',columns=columns,**constraints)

        try:
            results = ascii.read(results)
        except:
            return []

        if self.nearest is True:
            matrix = []
            for re in results:
                matrix.append([re['raMean'],re['decMean']])
            matrix = np.array(matrix)
            return_index = Utils().get_nearest(self.ra,self.dec,matrix)
            temp = []
            temp.append(results[return_index]['objID'])
            return temp

        else :
            return results['objID']

    def filter_id_to_str(self,filer_id):
        id2filter = np.array(list('grizy'))
        filer_str = id2filter[filer_id-1]
        return filer_str

    def ps1curves(self):
        """Get light curves of objects in specific radio with respect ra and dec, and possible return the object most nearest to radio
        Parameters
        ----------
        """
        ps1dic = ''
        first = True
        ids = self.ps1ids()
        if not any(ids):
            ps1dic = 'not found' # not object find
            return ps1dic

        dcolumns = ("""objID, detectID,filterID,obsTime,ra,dec,psfFlux,psfFluxErr,psfMajorFWHM,psfMinorFWHM,
                    psfQfPerfect,apFlux,apFluxErr,infoFlag,infoFlag2,infoFlag3""").split(',') 
        dcolumns = [x.strip() for x in dcolumns]
        dcolumns = [x for x in dcolumns if x and not x.startswith('#')]

        #split ids in dict
        for id in ids:
            dconstraints = {'objID': id}
            dresults = self.ps1search(format ='csv',table='detection',release='dr2',columns=dcolumns,**dconstraints)

            if first :
                dresults_ = ascii.read(dresults)
                filer_str = self.filter_id_to_str(dresults_['filterID'])
                mag = Utils().flux_to_mag(dresults_['psfFlux'])
                magerr = Utils().fluxerr_to_magerr(dresults_['psfFluxErr'],dresults_['psfFlux']) 
                ps1_matrix = np.array([dresults_['objID'],dresults_['ra'],dresults_['dec'],dresults_['obsTime'],mag,magerr,filer_str]).T
                first = False
            #
            else :
                dresults_ = ascii.read(dresults)
                filer_str = self.filter_id_to_str(dresults_['filterID'])
                mag = Utils().flux_to_mag(dresults_['psfFlux'])
                magerr = Utils().fluxerr_to_magerr(dresults_['psfFluxErr'],dresults_['psfFlux']) 
                ps1_matrix_aux = np.array([dresults_['objID'],dresults_['ra'],dresults_['dec'],dresults_['obsTime'],mag,magerr,filer_str]).T
                ps1_matrix = np.vstack((ps1_matrix,ps1_matrix_aux))
        return ps1_matrix

    def get_lc(self):
        """
        Get all ligth curves data or the most close object, inside degree area from PS1 catalog.
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
        data_return = self.ps1curves()
        return data_return