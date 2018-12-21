#!/usr/bin/env python
"""Top-level module for intake_cmip."""
from ._version import get_versions
from intake_cmip import database
from .cmip5 import CMIP5DataSource

__version__ = get_versions()["version"]
del get_versions

__all__ = ["intake_cmip", "database", "CMIP5DataSource",]
