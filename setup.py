#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages
import versioneer
from os.path import exists

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

if exists("README.rst"):
    with open("README.rst") as f:
        long_description = f.read()
else:
    long_description = ""


setup(
    maintainer="Anderson Banihirwe",
    maintainer_email="abanihi@ucar.edu",
    description="An intake plugin for loading CMIP5, CMIP6 data sets",
    python_requires=">3.5",
    install_requires=install_requires,
    license="Apache License 2.0",
    long_description=long_description,
    keywords=["cmip5", "cmip6" "intake"],
    name="intake-cmip",
    packages=find_packages(),
    py_modules=["intake_cmip"],
    package_data={"": ["*.csv"]},
    include_package_data=True,
    url="https://github.com/NCAR/intake-cmip",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    entry_points="""
      """,
    zip_safe=False,
)
