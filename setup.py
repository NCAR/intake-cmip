#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
import versioneer

with open("README.md", encoding="utf-8") as readme_file:
    readme = readme_file.read()

requirements = ["intake", "intake-xarray"]

setup(
    maintainer="Anderson Banihirwe",
    maintainer_email="abanihi@ucar.edu",
    description="An intake plugin for loading CMIP5 data sets",
    install_requires=requirements,
    license="Apache License 2.0",
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords=["cmip5", "intake"],
    name="intake-cmip5",
    packages=find_packages(),
    py_modules=["intake_cmip5"],
    #package_data={"": ["*.yml", "*.yaml", "*.csv"]},
    include_package_data=True,
    url="https://github.com/NCAR/intake-cmip5",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    entry_points="""
      """,
    zip_safe=False,
)
