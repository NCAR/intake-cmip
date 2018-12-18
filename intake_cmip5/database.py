
#!/usr/bin/env python
"""Contains functions to generate CMIP5 data sets database."""
import os
import pandas as pd
from dask import delayed
import re
from pathlib import Path
import functools
import dask.dataframe as dd
import shutil


HOME = os.environ["HOME"]
INTAKE_CMIP5_DIR = f"{HOME}/.intake_cmip5"


@functools.lru_cache(maxsize=1024, typed=False)
def _parse_dirs(root_dir):
    institution_dirs = [
        os.path.join(root_dir, activity, institution)
        for activity in os.listdir(root_dir)
        for institution in os.listdir(os.path.join(root_dir, activity))
        if os.path.isdir(os.path.join(root_dir, activity, institution))
    ]

    model_dirs = [
        os.path.join(institution_dir, model)
        for institution_dir in institution_dirs
        for model in os.listdir(institution_dir)
        if os.path.isdir(os.path.join(institution_dir, model))
    ]

    experiment_dirs = [
        os.path.join(model_dir, exp)
        for model_dir in model_dirs
        for exp in os.listdir(model_dir)
        if os.path.isdir(os.path.join(model_dir, exp))
    ]

    freq_dirs = [
        os.path.join(experiment_dir, freq)
        for experiment_dir in experiment_dirs
        for freq in os.listdir(experiment_dir)
        if os.path.isdir(os.path.join(experiment_dir, freq))
    ]

    realm_dirs = [
        os.path.join(freq_dir, realm)
        for freq_dir in freq_dirs
        for realm in os.listdir(freq_dir)
        if os.path.isdir(os.path.join(freq_dir, realm))
    ]

    return realm_dirs


def _get_entry(directory):
    dir_split = directory.split("/")
    entry = {}
    entry["realm"] = dir_split[-1]
    entry["frequency"] = dir_split[-2]
    entry["experiment"] = dir_split[-3]
    entry["model"] = dir_split[-4]
    entry["institution"] = dir_split[-5]
    return entry


@delayed
def _parse_directory(directory):
    exclude = set(["files", "latests"])  # directories to exclude

    columns = [
        "ensemble",
        "experiment",
        "file_basename",
        "file_fullpath",
        "frequency",
        "institution",
        "model",
        "root",
        "realm",
        "varname",
    ]
    df = pd.DataFrame(columns=columns)

    entry = _get_entry(directory)

    for root, dirs, files in os.walk(directory):
        # print(root)
        dirs[:] = [d for d in dirs if d not in exclude]
        if not files:
            continue
        sfiles = sorted([f for f in files if os.path.splitext(f)[1] == ".nc"])
        if not sfiles:
            continue

        fs = []
        for f in sfiles:
            try:
                f_split = f.split("_")
                entry["varname"] = f_split[0]
                entry["ensemble"] = f_split[-2]
                entry["root"] = root
                entry["file_basename"] = f
                entry["file_fullpath"] = os.path.join(root, f)
                fs.append(entry)
            except BaseException:
                continue
        if fs:
            temp_df = pd.DataFrame(fs)

        else:
            temp_df = pd.DataFrame()
            temp_df.columns = df.columns
        df = pd.concat([temp_df, df], ignore_index=True, sort=False)
    return df


def _persist_database(df, path):
    vYYYYMMDD = (
        r"v\d{4}\d{2}\d{2}"
    )  # TODO: Very dangerous in case the root dir matches the pattern
    vN = r"v\d{1}"
    v = re.compile("|".join([vYYYYMMDD, vN]))  # Combine both regex into one
    df["version"] = df.root.str.findall(v)
    df["version"] = df["version"].apply(lambda x: x[0] if x else "v0")
    sorted_df = (
        df.sort_values("version")
        .drop_duplicates(subset="file_basename", keep="last")
        .reset_index(drop=True)
    )

    if path:
        INTAKE_CMIP5_DIR = path

    print(f"**** Persisting CMIP5 database in {INTAKE_CMIP5_DIR} ****")

    if os.path.isdir(INTAKE_CMIP5_DIR):
        shutil.rmtree(INTAKE_CMIP5_DIR)
    os.makedirs(INTAKE_CMIP5_DIR, exist_ok=True)

    sorted_df.to_csv(f"{INTAKE_CMIP5_DIR}/clean_cmip5_database.csv", index=False)
    df.to_csv(f"{INTAKE_CMIP5_DIR}/raw_cmip5_database.csv", index=False)

    return sorted_df


def create_cmip5_database(root_dir=None, db_path=None):
    """Generates database for CMIP5 data sets
    
    Parameters
    ----------

    root_dir : string or file handle, default None
               File path or object

    db_path : string or file handle, default None
              File path or object, 
              # TODO: if None is provided the result is returned as a string.
    
    Raises
    ------

    NotADirectoryError
            if the `root_dir` does not exist
    
    Returns
    -------
        pd.DataFrame
    """

    if not os.path.exists(root_dir):
        raise NotADirectoryError(f"{root_dir} does not exist")

    dirs = _parse_dirs(root_dir)
    dfs = [_parse_directory(directory) for directory in dirs]
    df = dd.from_delayed(dfs).compute()
    df = _persist_database(df, db_path)
    return df
