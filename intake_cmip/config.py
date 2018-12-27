#!/usr/bin/env python
""" The configuration utility script. This script is used
to pass CMIP database/files to intake_cmip DataSources.
"""

from __future__ import absolute_import, print_function

import os

glade_cmip5_db = os.path.join(os.path.dirname(__file__), "cmip5.csv")
