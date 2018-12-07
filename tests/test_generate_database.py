import os
import pandas as pd
import xarray as xr
import pytest
import shutil
import tempfile
from intake_cmip5.generate_database import create_CMIP5Database
from pandas.testing import assert_frame_equal

HOME = os.environ["HOME"]
CMIP5_TEST_DIR = f"{HOME}/cmip5_test"
DB_DIR = tempfile.mkdtemp()


def setup():
    test_paths = [
        f"{CMIP5_TEST_DIR}/output1/CCCma/CanESM2/rcp85/mon/atmos/Amon/r2i1p1",
        f"{CMIP5_TEST_DIR}/output2/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/seaIce/OImon/r2i1p1/v1/sic",
    ]
    file_names = [
        "Tair_Amon_CanESM2_rcp85_r2i1p1_200601-203512.nc",
        "Tair_OImon_CSIRO-Mk3-6-0_historical_r2i1p1_200601-203512.nc",
    ]

    ds = (
        xr.tutorial.open_dataset("rasm")
        .load()
        .isel(time=slice(0, 2), x=slice(0, 5), y=slice(0, 3))
    )

    for idx, path in enumerate(test_paths):
        os.makedirs(path, exist_ok=True)
        file_path = f"{path}/{file_names[idx]}.nc"
        ds.to_netcdf(file_path, mode="w")


def teardown():
    try:
        shutil.rmtree(CMIP5_TEST_DIR)
    except:
        pass

    try:
        shutil.rmtree(DB_DIR)
    except:
        pass


setup()


def test_generate_database():
    res = create_CMIP5Database(CMIP5_TEST_DIR, DB_DIR)
    assert isinstance(res, pd.DataFrame)
    exp = pd.read_csv(f"{DB_DIR}/clean_cmip5_database.csv")
    assert_frame_equal(res, exp)


teardown()
