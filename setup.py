#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
import versioneer
from os.path import exists

readme = open('README.rst').read() if exists('README.rst') else ''

requirements = ["intake", "intake-xarray"]

setup(
    maintainer="Anderson Banihirwe",
    maintainer_email="abanihi@ucar.edu",
    description="An intake plugin for loading CMIP5, CMIP6 data sets",
    install_requires=requirements,
    license="Apache License 2.0",
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords=["cmip5","cmip6" "intake"],
    name="intake-cmip",
    packages=find_packages(),
    py_modules=["intake_cmip"],
    #package_data={"": ["*.yml", "*.yaml", "*.csv"]},
    include_package_data=True,
    url="https://github.com/NCAR/intake-cmip",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    entry_points="""
      """,
    zip_safe=False,
)
