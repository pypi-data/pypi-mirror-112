from Freya_alerce.catalogs.core.core import GetData

class DataLcDegree(GetData):
    """
    Parameters:
    ------------
    ra : (float) 
        Right ascension | example: ra=139.33444972
    dec :  (float) 
        Declination | example: dec=68.6350604
    radius: (float) 
        Search radius | example: radius=0.0002777
    format: (string) 
        [numpy,csv,votable] | example: format='csv'
    nearest: (bool)
        True or False | example: nearest=True
    """
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
    
    def get_data(self):
        """
        Return
        ------
        Return the LCs from the selected catalog in designated format.
        """
        return super().generic_call_data('get_lc_deg')

class DataLcHms(GetData):
    """
    Parameters:
    ------------
    hms : (string) 
        ICRS | example: hms = '9h17m20.26793280000689s +4h34m32.414496000003936s'
    radius: (float) 
        Search radius | example: radius=0.0002777
    format: (string) 
        [numpy,csv,votable] | example: format='csv'
    nearest: (bool)
        True or False | example: nearest=False
    """
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def get_data(self):
        """
        Return
        ------
        Return the LCs from the selected catalog in designated format.
        """
        return super().generic_call_data('get_lc_hms')