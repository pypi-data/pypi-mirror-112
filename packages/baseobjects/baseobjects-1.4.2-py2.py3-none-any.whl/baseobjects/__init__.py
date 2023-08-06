#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" __init__.py
baseobjects provides several base classes.
"""
__author__ = "Anthony Fong"
__copyright__ = "Copyright 2021, Anthony Fong"
__credits__ = ["Anthony Fong"]
__license__ = ""
__version__ = "1.4.2"
__maintainer__ = "Anthony Fong"
__email__ = ""
__status__ = "Production/Stable"

# Default Libraries #

# Downloaded Libraries #

# Local Libraries #
from .baseobject import BaseObject
from .basemeta import BaseMeta
from .objects import *
from .warnings import TimeoutWarning
