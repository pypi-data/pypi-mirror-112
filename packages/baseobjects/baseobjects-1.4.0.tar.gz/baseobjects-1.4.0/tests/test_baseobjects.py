#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" test_baseobjects.py
Test for the baseobjects package
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
import abc
import copy
import pathlib
import pickle
import timeit

# Downloaded Libraries #
import pytest

# Local Libraries #
import src.baseobjects as baseobjects


# Definitions #
# Functions #
@pytest.fixture
def tmp_dir(tmpdir):
    """A pytest fixture that turn the tmpdir into a Path object."""
    return pathlib.Path(tmpdir)


# Classes #
class ClassTest(abc.ABC):
    """Default class tests that all classes should pass."""
    class_ = None
    timeit_runs = 100000
    speed_tolerance = 200

    def test_instance_creation(self):
        pass


class TestInitMeta(ClassTest):
    class InitMetaTest(baseobjects.BaseObject, metaclass=baseobjects.InitMeta):
        one = 1

        @classmethod
        def _init_class_(cls):
             cls.one = 2

    def test_init_class(self):
        assert self.InitMetaTest.one == 2

    def test_meta(self):
        obj = self.InitMetaTest()
        obj.copy()


class BaseBaseObjectTest(ClassTest):
    """All BaseObject subclasses need to base these tests to considered functional."""
    pass


class TestBaseObject(BaseBaseObjectTest):
    """Test the BaseObject class which a subclass is created to test with."""
    class BaseTestObject(baseobjects.BaseObject):
        def __init__(self):
            self.immutable = 0
            self.mutable = {}

    class NormalObject(object):
        def __init__(self):
            self.immutable = 0
            self.mutable = {}

    class_ = BaseTestObject

    @pytest.fixture
    def test_object(self):
        return self.class_()

    def test_copy(self, test_object):
        new = test_object.copy()
        assert id(new.immutable) == id(test_object.immutable)
        assert id(new.mutable) == id(test_object.mutable)

    def test_deepcopy(self, test_object):
        new = test_object.deepcopy()
        assert id(new.immutable) == id(test_object.immutable)
        assert id(new.mutable) != id(test_object.mutable)

    def test_copy_speed(self, test_object):
        normal = self.NormalObject()

        def normal_copy():
            copy.copy(normal)

        mean_new = timeit.timeit(test_object.copy, number=self.timeit_runs) / self.timeit_runs * 1000000
        mean_old = timeit.timeit(normal_copy, number=self.timeit_runs) / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        print(f"\nNew speed {mean_new:.3f} μs took {percent:.3f}% of the time of the old function.")
        assert percent < self.speed_tolerance

    def test_deepcopy_speed(self, test_object):
        normal = self.NormalObject()

        def normal_deepcopy():
            copy.deepcopy(normal)

        mean_new = timeit.timeit(test_object.deepcopy, number=self.timeit_runs) / self.timeit_runs * 1000000
        mean_old = timeit.timeit(normal_deepcopy, number=self.timeit_runs) / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        print(f"\nNew speed {mean_new:.3f} μs took {percent:.3f}% of the time of the old function.")
        assert percent < self.speed_tolerance


class BaseWrapperTest(BaseBaseObjectTest):
    class ExampleOne:
        def __init__(self):
            self.one = "one"
            self.two = "one"

        def __eq__(self, other):
            return True

        def method(self):
            return "one"

    class ExampleTwo:
        def __init__(self):
            self.one = "two"
            self.three = "two"

        def function(self):
            return "two"

    class NormalWrapper:
        def __init__(self, first):
            self._first = first
            self.four = "wrapper"

        @property
        def one(self):
            return self._first.one

    class_ = None

    def new_object(self):
        pass

    def pickle_object(self):
        obj = self.new_object()
        pickle_jar = pickle.dumps(obj)
        new_obj = pickle.loads(pickle_jar)
        assert set(dir(new_obj)) == set(dir(obj))

    @pytest.fixture(params=[new_object])
    def test_object(self, request):
        return request.param(self)

    def test_instance_creation(self):
        pass

    def test_pickling(self, test_object):
        pickle_jar = pickle.dumps(test_object)
        new_obj = pickle.loads(pickle_jar)
        assert set(dir(new_obj)) == set(dir(test_object))

    def test_copy(self, test_object):
        new = test_object.copy()
        assert id(new._first) == id(test_object._first)

    def test_deepcopy(self, test_object):
        new = test_object.deepcopy()
        assert id(new._first) != id(test_object._first)

    def test_wrapper_overrides(self, test_object):
        assert test_object.two == "wrapper"
        assert test_object.four == "wrapper"
        assert test_object.wrap() == "wrapper"

    def test_example_one_overrides(self, test_object):
        assert test_object.one == "one"
        assert test_object.method() == "one"

    def test_example_two_overrides(self, test_object):
        assert test_object.three == "two"
        assert test_object.function() == "two"

    def test_setting_wrapped(self, test_object):
        test_object.one = "set"
        assert test_object._first.one == "set"

    def test_deleting_wrapped(self, test_object):
        del test_object.one
        assert "one" not in dir(test_object._first)

    @pytest.mark.xfail
    def test_magic_inheritance(self, test_object):
        assert test_object == 1

    @pytest.mark.xfail
    def test_local_access_speed(self, test_object):
        normal = self.NormalWrapper(self.ExampleOne())

        def new_access():
            getattr(test_object, "four")

        def old_access():
            getattr(normal, "four")

        mean_new = timeit.timeit(new_access, number=self.timeit_runs) / self.timeit_runs * 1000000
        mean_old = timeit.timeit(old_access, number=self.timeit_runs) / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        print(f"\nNew speed {mean_new:.3f} μs took {percent:.3f}% of the time of the old function.")
        assert percent < self.speed_tolerance

    @pytest.mark.xfail
    def test_access_speed(self, test_object):
        normal = self.NormalWrapper(self.ExampleOne())

        def new_access():
            getattr(test_object, "one")

        def old_access():
            getattr(getattr(normal, "_first"), "one")

        mean_new = timeit.timeit(new_access, number=self.timeit_runs) / self.timeit_runs * 1000000
        mean_old = timeit.timeit(old_access, number=self.timeit_runs) / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        print(f"\nNew speed {mean_new:.3f} μs took {percent:.3f}% of the time of the old function.")
        assert percent < self.speed_tolerance

    @pytest.mark.xfail
    def test_property_access_speed(self, test_object):
        normal = self.NormalWrapper(self.ExampleOne())

        def new_access():
            getattr(normal, "one")

        def old_access():
            getattr(getattr(normal, "_first"), "one")

        mean_new = timeit.timeit(new_access, number=self.timeit_runs) / self.timeit_runs * 1000000
        mean_old = timeit.timeit(old_access, number=self.timeit_runs) / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        print(f"\nNew speed {mean_new:.3f} μs took {percent:.3f}% of the time of the old function.")
        assert percent < self.speed_tolerance

    @pytest.mark.xfail
    def test_vs_property_access_speed(self, test_object):
        normal = self.NormalWrapper(self.ExampleOne())

        def new_access():
            getattr(test_object, "one")

        def old_access():
            getattr(normal, "one")

        mean_new = timeit.timeit(new_access, number=self.timeit_runs) / self.timeit_runs * 1000000
        mean_old = timeit.timeit(old_access, number=self.timeit_runs) / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        print(f"\nNew speed {mean_new:.3f} μs took {percent:.3f}% of the time of the old function.")
        assert percent < self.speed_tolerance


class TestStaticWrapper(BaseWrapperTest):
    class StaticWrapperTestObject1(baseobjects.StaticWrapper):
        _wrapped_types = [BaseWrapperTest.ExampleOne(), BaseWrapperTest.ExampleTwo()]
        _wrap_attributes = ["_first", "_second"]

        def __init__(self, first=None, second=None):
            self._first = first
            self._second = second
            self.two = "wrapper"
            self.four = "wrapper"

        def wrap(self):
            return "wrapper"

    class StaticWrapperTestObject2(baseobjects.StaticWrapper):
        _set_next_wrapped = True
        _wrap_attributes = ["_first", "_second"]

        def __init__(self, first=None, second=None):
            self.two = "wrapper"
            self.four = "wrapper"
            self._first = first
            self._second = second
            self._wrap()

        def wrap(self):
            return "wrapper"

    class_ = StaticWrapperTestObject1

    def new_object_1(self):
        first = self.ExampleOne()
        second = self.ExampleTwo()
        return self.StaticWrapperTestObject1(first, second)

    def new_object_2(self):
        first = self.ExampleOne()
        second = self.ExampleTwo()
        return self.StaticWrapperTestObject2(first, second)

    @pytest.fixture(params=[new_object_1, new_object_2])
    def test_object(self, request):
        return request.param(self)


class TestDynamicWrapper(BaseWrapperTest):
    class DynamicWrapperTestObject(baseobjects.DynamicWrapper):
        _wrap_attributes = ["_first", "_second"]

        def __init__(self, first=None, second=None):
            self._first = first
            self._second = second
            self.two = "wrapper"
            self.four = "wrapper"

        def wrap(self):
            return "wrapper"

    class_ = DynamicWrapperTestObject

    def new_object(self):
        first = self.ExampleOne()
        second = self.ExampleTwo()
        return self.DynamicWrapperTestObject(first, second)

    @pytest.fixture(params=[new_object])
    def test_object(self, request):
        return request.param(self)


# Main #
if __name__ == '__main__':
    pytest.main(["-v", "-s"])
