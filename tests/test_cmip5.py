import os
import shutil
import tempfile

import pandas as pd
import pytest
import xarray as xr
from pandas.testing import assert_frame_equal

from intake_cmip.cmip5 import CMIP5DataSource
from intake_cmip.database import create_cmip5_database

CMIP5_TEST_DIR = tempfile.mkdtemp()
DB_DIR = tempfile.mkdtemp()
file_names = [
    "Tair_Amon_CanESM2_rcp85_r2i1p1_200601-203512.nc",
    "Tair_OImon_CSIRO-Mk3-6-0_historical_r2i1p1_200601-203512.nc",
]


def setup():
    test_paths = [
        f"{CMIP5_TEST_DIR}/output1/CCCma/CanESM2/rcp85/mon/atmos/Amon/r2i1p1",
        f"{CMIP5_TEST_DIR}/output2/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/seaIce/OImon/r2i1p1/v1/sic",
    ]

    ds = (
        xr.tutorial.open_dataset("rasm")
        .load()
        .isel(time=slice(0, 2), x=slice(0, 5), y=slice(0, 3))
    )

    for idx, path in enumerate(test_paths):
        os.makedirs(path, exist_ok=True)
        file_path = f"{path}/{file_names[idx]}"
        ds.to_netcdf(file_path, mode="w")


def teardown():
    try:
        shutil.rmtree(CMIP5_TEST_DIR)
    except BaseException:
        pass

    try:
        shutil.rmtree(DB_DIR)
    except BaseException:
        pass


def test_generate_database():
    setup()
    df_res = create_cmip5_database(CMIP5_TEST_DIR, DB_DIR)
    assert isinstance(df_res, pd.DataFrame)

    df_exp = pd.read_csv(f"{DB_DIR}/cmip5.csv")

    assert_frame_equal(df_res, df_exp)

    exp = set(file_names)
    res = set(df_exp.file_basename.unique().tolist())

    assert exp == res
    teardown()


def test_source():
    setup()
    create_cmip5_database(CMIP5_TEST_DIR, DB_DIR)
    db_file = f"{DB_DIR}/cmip5.csv"
    source = CMIP5DataSource(
        database_file=db_file,
        model="CanESM2",
        experiment="rcp85",
        frequency="mon",
        realm="atmos",
        ensemble="r2i1p1",
        varname="Tair",
    )
    assert isinstance(source, CMIP5DataSource)

    ds = source.to_dask()
    assert isinstance(ds, xr.Dataset)
    teardown()
