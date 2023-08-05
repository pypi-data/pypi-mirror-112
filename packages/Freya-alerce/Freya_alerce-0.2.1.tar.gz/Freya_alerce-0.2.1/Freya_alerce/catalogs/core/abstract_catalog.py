from abc import ABC, abstractmethod

class BaseCatalog(ABC):

    @abstractmethod
    def get_lc():
        """
       Get all ligth curves data or the most close object, inside degree area.

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
        return ""
