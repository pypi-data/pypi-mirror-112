import pandas as pd
import io

from astropy.io.votable import from_table, writeto
from astropy.io.votable.tree import VOTableFile, Table
from astropy.table import Table, Column

class FormatLC(object):
    """
    Parameters
    ----------
    data_np : numpy array 2d
        input is numpy array 2d, each column is a feature (['obj','ra','dec','mjd','mag',''magerr,'filter','catalog']), each column is an observation of a object.
    """

    def __init__(self,data_np):
        self.data_np = data_np

    def format_numpy(self):
        """
        Return
        -------
        Return data who numpy matrix.
        """
        return self.data_np

    def format_csv(self):
        """
        Return
        -------
        Return data in CSV format.
        """
        df = pd.DataFrame({'obj':self.data_np[:,0],'ra':self.data_np[:,1],
                            'dec':self.data_np[:,2],'mjd':self.data_np[:,3],
                            'mag':self.data_np[:,4],'magerr':self.data_np[:,5],
                            'filter':self.data_np[:,6],'catalog':self.data_np[:,7]})
        return df.to_csv(index=False)

    def format_votable(self):
        """
        Return
        -------
        Return data in VOTable format.
        """
        names_column = ['obj','ra','dec','mjd','mag','magerr','filter','catalog']
        descriptions_column = ['Id of object in catalog the original catalog',
                                'Right ascension of source','Declination of source',
                                'Julian Day','Magnitude','Magnitude Error',
                                'Filter code','Original Catalog']
        #dtype_column = [] # dtype=dtype_column
        t = Table(rows=self.data_np,names=names_column,descriptions=descriptions_column)
        votable= VOTableFile.from_table(t)
        buf = io.BytesIO()
        writeto(votable,buf)
        return buf.getvalue().decode("utf-8")