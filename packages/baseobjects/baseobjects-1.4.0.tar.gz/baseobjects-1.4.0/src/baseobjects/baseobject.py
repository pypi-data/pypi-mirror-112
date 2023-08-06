#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" baseobject.py
BaseObject is an abstract class which implements some basic methods that all objects should have.
"""
__author__ = "Anthony Fong"
__copyright__ = "Copyright 2021, Anthony Fong"
__credits__ = ["Anthony Fong"]
__license__ = ""
__version__ = "1.4.0"
__maintainer__ = "Anthony Fong"
__email__ = ""
__status__ = "Production/Stable"

# Default Libraries #
from abc import ABC
from copy import _copy_dispatch, _copy_immutable, _deepcopy_dispatch, _deepcopy_atomic, _keep_alive, _reconstruct, Error
from copyreg import dispatch_table

# Downloaded Libraries #

# Local Libraries #


# Definitions #
# Classes #
class BaseObject(ABC):
    """An abstract class that implements some basic methods that all objects should have."""

    # Magic Methods
    # Construction/Destruction
    def __copy__(self):
        """The copy magic method (shallow).

        Returns:
            :obj:`BaseObject`: A shallow copy of this object.
        """
        cls = type(self)

        copier = _copy_dispatch.get(cls)
        if copier:
            return copier(self)

        if issubclass(cls, type):
            # treat it as a regular class:
            return _copy_immutable(self)

        reductor = dispatch_table.get(cls)
        if reductor is not None:
            rv = reductor(self)
        else:
            reductor = getattr(self, "__reduce_ex__", None)
            if reductor is not None:
                rv = reductor(4)
            else:
                reductor = getattr(self, "__reduce__", None)
                if reductor:
                    rv = reductor()
                else:
                    raise Error("un(shallow)copyable object of type %s" % cls)

        if isinstance(rv, str):
            return self
        return _reconstruct(self, None, *rv)

    def __deepcopy__(self, memo=None, _nil=[]):
        """The deepcopy magic method

        Args:
            memo (dict): A dictionary of user defined information to pass to another deepcopy call which it will handle.

        Returns:
            :obj:`BaseObject`: A deep copy of this object.
        """
        if memo is None:
            memo = {}

        d = id(self)
        y = memo.get(d, _nil)
        if y is not _nil:
            return y

        cls = type(self)

        # If copy method is in the deepcopy dispatch then use it
        copier = _deepcopy_dispatch.get(cls)
        if copier is not None:
            y = copier(self, memo)
        else:
            # Handle if this object is a type subclass
            if issubclass(cls, type):
                y = _deepcopy_atomic(self, memo)
            else:
                reductor = dispatch_table.get(cls)
                if reductor:
                    rv = reductor(self)
                else:
                    reductor = getattr(self, "__reduce_ex__", None)
                    if reductor is not None:
                        rv = reductor(4)
                    else:
                        reductor = getattr(self, "__reduce__", None)
                        if reductor:
                            rv = reductor()
                        else:
                            raise Error("un(deep)copyable object of type %s" % cls)
                if isinstance(rv, str):
                    y = self
                else:
                    y = _reconstruct(self, memo, *rv)

        # If is its own copy, don't memoize.
        if y is not self:
            memo[d] = y
            _keep_alive(self, memo)  # Make sure x lives at least as long as d

        return y

    # Instance Methods
    # Constructors/Destructors
    def copy(self):
        """Creates a shallow copy of this object.

        Returns:
            A shallow copy of this object.
        """
        return self.__copy__()

    def deepcopy(self, memo={}):
        """Creates a deep copy of this object.

        Args:
            memo (dict): A dictionary of user defined information to pass to another deepcopy call which it will handle.

        Returns:
            A deep copy of this object.
        """
        return self.__deepcopy__(memo=memo)
