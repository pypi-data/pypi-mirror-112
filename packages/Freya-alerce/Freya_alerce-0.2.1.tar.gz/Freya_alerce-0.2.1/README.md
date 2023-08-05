# Here it is the module python 'Freya'.
Freya is a Fremework <3, and this github is the python code.

# Start (Commands CLI). 🚀
With Freya get light curve data is more simple.
Have option by CLI 'freya-admin', the options are:
  
  * Creates new catalog who module inside Freya, where name is the name of catalog what choose and source
  is where it comes from (available options: api,db).
  ```
  freya-admin --newcatalog <name> <source>
  ```
  * Creates new api called FreyaAPI in path with call freya-admin, this opcion create a new flask application with
  all rutes necessaries.
  ```
  freya-admin --newapi
  ```
  * Rename catalog inside Freya, replace old_name for new_name in all files inside module-catalog and the folder name.
  ```
  freya-admin --renamecatalog <old_name> <new_name>
  ```
  * Delete catalog inside Freya.
  ```
  freya-admin --deletecatalog <name>
  ```
  * Add new resource in FreyaAPI, but first need whit catalog exist in Freya or local folder and the call --addresource
  inside the folder FreyaAPI.
  ```
  freya-admin --addresource <name> 
  ```
  * And want creates new catalog who local module, can use --newcataloglocal.
  where name is the name of catalog what choose and source is where it comes from (available options: api,db).
  ```
  freya-admin --newcataloglocal <name> <source>

  # then install module
    pip install .
  ```
* Important: the name register with in capital letters, but you can use lowercase name.
# Install Freya. 🔧

```
pip install Freya_alerce

#or clone repository and 

pip install .  or python setup.py install


```
Before install Freya can use the comand
```
python setup.py test 
```
## Add new catalogs in Freya or local. 🔧
* If you want add modules catalogs inside Freya use for example:
```
freya-admin --newcatalog ztf api

```
* If you want use local module:
```
# Inside local folder catalogs
freya-admin --newcataloglocal ztf_local api

# then use

pip install .

```
* If you download any catalog for the github or other site you can install in environment python.
```
pip install .
```

Independet how add catalog the next step is to connect catalog with Freya (if not completed before),
for this need completed one generic method.
```
Inside folder new catalog find the following files
- configure.py
- methods.py 
- connect.py (if source is 'db') 

now inside 'configure.py' it find 

  - def get_lc(ra,dec,radius,nearest)

Need to be completed such that
    - def get_lc_deg(ra,dec,radius,nearest)
        return all light curves data from all object find in area 
        described in degrees with specific radius or return the data
        from object most close. 

        Then need return numpy array 2d with rows represent the objects and columns : ['obj','ra','dec','mjd','mg','filter'].
            obj : double
                Id of object in catalog
            ra : float
                Right ascension
            dec : float
                Declination
            mjd : float
                Julian day
            mg : float
                Magnitud
            filter : str
                Band 
```
* For example, ztf is default catalog inside in Freya. 

'~/Freya/catalogs/ztf/configure.py'
```python

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
    
```


And if you use catalog with source data base, need complete 'connect.py'
```
# Inside file connect.py
 - user
 - password
 - host
 - port
 - database
```
## Catalogs Default 📖 

Inside Freya you can find the ZTF-Dr3 and PS1-Dr2 catalogs.

## How use a only Freya
If you want use Freya but without installing, you can use Freya's methods "DataLcDegree(),DataLcHms()".
```
from Freya_alerce.catalogs.core.data_lc import DataLcDegree,DataLcHms

data_all_deg = DataLcDegree(catalog,ra,dec,radius,format,nearest).get_data()
data_one_deg = DataLcDegree(catalog,ra,dec,radius,format,nearest).get_data()
data_all_hms = DataLcHms(catalog,radius,format,nearest).get_data()
data_one_hms = DataLcHms(catalog,radius,format,nearest).get_data()
```
Reed the demo in this gitHub for complete example.
# FreyaAPI

If use the FreyaAPI, you can create the new API with CLI freya-admin or 
donwload from the github [FreyaAPI](https://github.com/fernandezeric/FreayaAPI).

Into github have the instruction of the use FreyaAPI, and how to as add the new resources with the freya-admin.


# Build with 🛠️
* Python : 3.9
###
Jonimott de Malpais - [fernandezeric](https://github.com/fernandezeric)
