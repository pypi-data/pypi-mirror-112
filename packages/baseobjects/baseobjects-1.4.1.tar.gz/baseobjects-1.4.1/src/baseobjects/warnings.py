#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" warnings.py
Adds additional Warnings.
"""
__author__ = "Anthony Fong"
__copyright__ = "Copyright 2021, Anthony Fong"
__credits__ = ["Anthony Fong"]
__license__ = ""
__version__ = "1.4.1"
__maintainer__ = "Anthony Fong"
__email__ = ""
__status__ = "Production/Stable"

# Default Libraries #

# Downloaded Libraries #

# Local Libraries #


# Definitions #
# Classes #
class TimeoutWarning(Warning):
    """A general warning for timeouts."""

    # Magic Methods
    # Construction/Destruction
    def __init__(self, name="A function"):
        message = f"{name} timed out"
        super().__init__(message)
