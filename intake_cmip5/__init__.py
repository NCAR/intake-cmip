#!/usr/bin/env python
"""Top-level module for intake_cmip5."""
from ._version import get_versions
import intake_cmip5
from intake_cmip5 import database
from intake_cmip5.source import CMIP5DataSource

__version__ = get_versions()["version"]
del get_versions

__all__ = ["intake_cmip5", "database", "CMIP5DataSource",]
