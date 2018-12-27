#!/usr/bin/env python
import os
from collections import OrderedDict

import intake_xarray.base
import numpy as np
import pandas as pd
import xarray as xr

from ._version import get_versions
from .config import glade_cmip5_db

__version__ = get_versions()["version"]
del get_versions


class CMIP5DataSource(intake_xarray.base.DataSourceMixin):
    """ Read CMIP5 data sets into xarray datasets

    """

    container = "xarray"
    version = __version__
    partition_access = True
    name = "cmip5"

    def __init__(
        self,
        database,
        model,
        experiment,
        frequency,
        realm,
        ensemble,
        varname,
        metadata=None,
    ):
        """

        Parameters
        ----------

        database : string or file handle
             File path or object for cmip5 database. For users with access to
             NCAR's glade file system, this argument can be set to 'glade'.
        model : str
              identifies the model used (e.g. HADCM3, HADCM3-233).
        experiment : str
             identifies either the experiment or both the experiment family and a specific type
             within that experiment family.
        frequency : str
            indicates the interval between individual time-samples in the atomic dataset.
            For CMIP5, the following are the only options:

            - yr
            - mon
            - day
            - 6hr
            - 3hr
            - subhr
            - monClim
            - fx

        realm : str
             indicates which high level modeling component is of particular relevance for
             the dataset. For CMIP5, permitted values are:

             - atmos
             - ocean
             - land
             - landIce
             - seaIce
             - aerosol
             - atmosChem
            - ocnBgchem
        ensemble : str
            (r<N>i<M>p<L>): This triad of integers (N, M, L), formatted as (e.g., “r3i1p21”)
            distinguishes among closely related simulations by a single model.
            All three are required even if only a single simulation is performed.
        varname : str

        """

        # store important kwargs
        self.database = self._read_database(database)
        self.model = model
        self.experiment = experiment
        self.frequency = frequency
        self.realm = realm
        self.ensemble = ensemble
        self.varname = varname
        self.urlpath = ""
        self._ds = None
        super(CMIP5DataSource, self).__init__(metadata=metadata)

    def _read_database(self, database):
        if database == "glade":
            database = glade_cmip5_db
        if os.path.exists(database):
            return pd.read_csv(database)
        else:
            raise FileNotFoundError(f"{database}")

    def _open_dataset(self):
        ens_filepaths = get_ens_filepaths(
            self.database,
            self.model,
            self.experiment,
            self.frequency,
            self.realm,
            self.ensemble,
            self.varname,
        )

        ds_list = [xr.open_mfdataset(paths) for paths in ens_filepaths.values()]
        ens_list = list(ens_filepaths.keys())
        self._ds = xr.concat(ds_list, dim="ensemble")
        self._ds["ensemble"] = ens_list

    def to_xarray(self, dask=True):
        """Return dataset as an xarray instance"""
        if dask:
            return self.to_dask()
        return self.read()


def get_ens_filepaths(database, model, experiment, frequency, realm, ensemble, varname):
    query = {
        "model": model,
        "experiment": experiment,
        "frequency": frequency,
        "realm": realm,
        "ensemble": ensemble,
        "varname": varname,
    }

    condition = np.ones(len(database), dtype=bool)

    for key, val in query.items():
        if val is not None:

            condition = condition & (database[key] == val)

    database_subset = database.loc[condition]

    if database_subset.empty:

        raise ValueError(
            f"No dataset found for:\n \
                              \tmodel = {model} \n \
                              \texperiment = {experiment} \n \
                              \tfrequency = {frequency} \n \
                              \trealm = {realm} \n \
                              \tensemble = {ensemble} \n \
                              \tvarname = {varname}"
        )

    # -- realm is optional arg so check that the same varname is not in multiple realms
    realm_list = database_subset.realm.unique()
    if len(realm_list) != 1:
        raise ValueError(
            f"{varname} found in multiple realms:\n \
                          '\t{realm_list}. Please specify the realm to use"
        )

    ds_dict = OrderedDict()
    for ens in database_subset["ensemble"].unique():
        ens_match = database_subset["ensemble"] == ens
        paths = database_subset.loc[ens_match]["file_fullpath"].tolist()
        ds_dict[ens] = paths

    return ds_dict
