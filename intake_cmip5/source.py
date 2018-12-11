import pandas as pd
import os
import numpy as np
import xarray as xr
import intake_xarray.base
from collections import OrderedDict

class CMIP5DataSource(intake_xarray.base.DataSourceMixin):
    container = 'xarray'
    version = '0.0.1'
    partition_access = True
    name = 'cmip5'
    
    def __init__(self, database_file, model, experiment, frequency, realm, ensemble, 
                 varname, metadata=None):
        # store important kwargs
        self.database = self._read_database(database_file)
        self.model = model
        self.experiment = experiment
        self.frequency = frequency
        self.realm = realm
        self.ensemble = ensemble
        self.varname = varname
        super(CMIP5DataSource, self).__init__(metadata=metadata)
        
    def _read_database(self, database_file):
        if os.path.exists(database_file):
            return pd.read_csv(database_file)
        else:
            raise FileNotFoundError(f"{database_file}")
            
    def _open_dataset(self):
        ens_filepaths = get_ens_filepaths(self.database, self.model, self.experiment, 
                          self.frequency, self.realm, self.ensemble, self.varname)
        
        
        ds_list = [xr.open_mfdataset(paths) for paths in ens_filepaths.values()]
        ens_list = list(ens_filepaths.keys())
        self._ds = xr.concat(ds_list, dim='ensemble')
        self._ds['ensemble'] = ens_list
    


    
def get_ens_filepaths(database, model, experiment, frequency, realm, ensemble, varname):
    query = {'model': model,
                'experiment': experiment,
                'frequency': frequency,
                'realm': realm,
                'ensemble': ensemble,
                'varname': varname}
    
    condition = np.ones(len(database), dtype=bool)
    
    for key, val in query.items():
        if val is not None:
                
            condition = condition & (database[key] == val)
        
    database_subset = database.loc[condition]
    
    if database_subset.empty:
        
        raise ValueError(f"No dataset found for:\n \
                              \tmodel = {model} \n \
                              \texperiment = {experiment} \n \
                              \tfrequency = {frequency} \n \
                              \trealm = {realm} \n \
                              \tensemble = {ensemble} \n \
                              \tvarname = {varname}")
        
    #-- realm is optional arg so check that the same varname is not in multiple realms
    realm_list = database_subset.realm.unique()
    if len(realm_list) != 1:
        raise ValueError(f"{varname} found in multiple realms:\n \
                          '\t{realm_list}. Please specify the realm to use")
        
        
    ds_dict = OrderedDict()
    for ens in database_subset['ensemble'].unique():
        ens_match = (database_subset['ensemble'] == ens)
        paths = database_subset.loc[ens_match]['file_fullpath'].tolist()
        ds_dict[ens] = paths
        
    return ds_dict

