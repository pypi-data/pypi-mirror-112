========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/python-baseobjects/badge/?style=flat
    :target: https://python-baseobjects.readthedocs.io/
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.com/fonganthonym/python-baseobjects.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.com/github/fonganthonym/python-baseobjects

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/fonganthonym/python-baseobjects?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/fonganthonym/python-baseobjects

.. |requires| image:: https://requires.io/github/fonganthonym/python-baseobjects/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/fonganthonym/python-baseobjects/requirements/?branch=master

.. |codecov| image:: https://codecov.io/gh/fonganthonym/python-baseobjects/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/fonganthonym/python-baseobjects

.. |version| image:: https://img.shields.io/pypi/v/baseobjects.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/baseobjects

.. |wheel| image:: https://img.shields.io/pypi/wheel/baseobjects.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/baseobjects

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/baseobjects.svg
    :alt: Supported versions
    :target: https://pypi.org/project/baseobjects

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/baseobjects.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/baseobjects

.. |commits-since| image:: https://img.shields.io/github/commits-since/fonganthonym/python-baseobjects/v1.4.0.svg
    :alt: Commits since latest release
    :target: https://github.com/fonganthonym/python-baseobjects/compare/v1.4.0...master



.. end-badges

Basic object templates.

* Free software: MIT license

Installation
============

::

    pip install baseobjects

You can also install the in-development version with::

    pip install https://github.com/fonganthonym/python-baseobjects/archive/master.zip


Documentation
=============


https://python-baseobjects.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
