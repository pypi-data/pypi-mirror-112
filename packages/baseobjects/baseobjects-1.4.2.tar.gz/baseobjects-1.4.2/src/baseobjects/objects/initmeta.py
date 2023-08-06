#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" initmeta.py
InitMeta is an abstract metaclass that implements an init class method which allows some setup after a class is created.
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
from ..basemeta import BaseMeta


# Definitions #
# Classes #
class InitMeta(BaseMeta):
    """An abstract metaclass that implements an init class method which allows some setup after a class is created."""

    # Magic Methods
    # Construction/Destruction
    def __new__(mcs, name, bases, namespace, **kwargs):
        cls = super().__new__(mcs, name, bases, namespace, **kwargs)
        cls._init_class_()
        return cls
