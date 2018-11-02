#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
import versioneer

with open("README.md", encoding="utf-8") as readme_file:
    readme = readme_file.read()

requirements = open('requirements.txt').read().strip().split('\n')

setup(
    maintainer="Anderson Banihirwe",
    maintainer_email="abanihi@ucar.edu",
    description='CMIP5 data and plugins for Intake',
    install_requires=requirements,
    license="https://github.com/NCAR/cmip5-intake-datasets/blob/master/LICENSE.rst",
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords=["cmip5", "intake"],
    name="cmip5-intake",
    packages=find_packages(),
    py_modules=['cmip5_intake'],
    package_data={'': ['*.yml', '*.yaml']},
    include_package_data=True,
    url="https://github.com/NCAR/cmip5-intake-datasets",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    entry_points="""
      [console_scripts]
      cmip5-intake-cat-gen=cmip5_intake.generate_catalog:generator
      """,
    zip_safe=False,
)