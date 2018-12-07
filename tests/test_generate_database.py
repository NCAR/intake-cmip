import os
import pandas as pd
HOME=os.environ["HOME"]
CMIP5_TEST_DIR=f"{HOME}/cmip5_test"


def generate_data():
    test_paths = [f"{CMIP5_TEST_DIR}/output1/CCCma/CanESM2/rcp85/mon/atmos/Amon/r2i1p1",
              f"{CMIP5_TEST_DIR}/output2/CSIRO-QCCCE/CSIRO-Mk3-6-0/historical/mon/seaIce/OImon/r2i1p1/v1/sic"]
    
    ds = xr.tutorial.load_dataset('rasm').isel(time=slice(0, 2), x=slice(0, 5), y=slice(0, 3))
    
    for idx, path in enumerate(test_paths):
        os.makedirs(path, exist_ok=True)
        file_path = f"{path}/var{idx}.nc"
        ds.to_netcdf(file_path, mode='w')
    