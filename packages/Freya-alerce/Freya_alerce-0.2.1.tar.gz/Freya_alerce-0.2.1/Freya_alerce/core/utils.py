
import numpy as np
from astropy.coordinates import SkyCoord
from astropy import units as u
"""
This class represent the generic methods
"""
class Utils:

    def deg_to_hms(self,ra,dec):
        """
        Transform degree point(ra,dec) in IRCS point(hms).
        Parameters
        ----------
        ra : float

        dec: float
        Return
        ---------
        Return point in string
        """
        coord_icrs = SkyCoord(ra=ra*u.degree, dec=dec*u.degree)
        return coord_icrs.to_string('hmsdms')

    def hms_to_deg(self,hms):
        """
        Transform IRCS point(hms) in degree point(ra,dec).
        Parameters
        ----------
        hms : string
        Return
        ---------
        Return two float values: 'ra' and 'deg'
        """
        coord = SkyCoord(hms,frame='icrs') #transform coord
        ra = coord.ra.degree
        dec = coord.dec.degree
        return ra,dec

    def get_nearest(self,center_ra,center_dec,matrix_ra_dec):
        """
        Transform degree point(ra,dec) in IRCS point(hms).
        Parameters
        ----------
        center_ra : float
        
        center_dec: float

        matrix_ra_dec : numpy array 2d values
            matrix in two dimension with column ra dec and the row represent the object, 
        Return
        ----------
        Return the index of matrix for the min angle between ra | dec center point and ra | dec the object.
        """
        angle = []
        c1 = SkyCoord(ra=center_ra,dec=center_dec,unit=u.degree)
        for obj in matrix_ra_dec:
            c2 = SkyCoord(obj[0],obj[1],unit=u.degree)
            angle.append(c1.separation(c2))
        return angle.index(min(angle))

    def flux_to_mag(self,psfFlux):
        """
        Convert psfFlux in AB magnitude, use [-2.5*np.log10(psfFlux) + 8.90].
        Parameters
        ----------
        psfFlux : numpy array
            psfFlux in janskys
        
        Return
        ----------
        Return numpy array with mag
        """
        mag = (-2.5*np.log10(psfFlux))+8.90
        return mag
    
    def fluxerr_to_magerr(self,psfFluxerror,psfFlux):
        """
        Convert psfFlux and psfFluxerr in AB mag, use [1.08574*(psfFluxerror / psfFlux)] for calcule magerr.
        Parameters
        ----------
        psfFluxerror : numpy array
            psfFluxerror in janskys
        psfFlux : numpy array
            psfFlux in janskys
        
        Return
        ----------
        Return numpy array with magerr 
        """
        magerr = 1.08574*(psfFluxerror/psfFlux) 
        return magerr