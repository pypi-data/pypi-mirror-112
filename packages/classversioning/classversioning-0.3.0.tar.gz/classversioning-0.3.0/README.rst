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
.. |docs| image:: https://readthedocs.org/projects/python-classversioning/badge/?style=flat
    :target: https://python-classversioning.readthedocs.io/
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.com/fonganthonym/python-classversioning.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.com/github/fonganthonym/python-classversioning

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/fonganthonym/python-classversioning?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/fonganthonym/python-classversioning

.. |requires| image:: https://requires.io/github/fonganthonym/python-classversioning/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/fonganthonym/python-classversioning/requirements/?branch=master

.. |codecov| image:: https://codecov.io/gh/fonganthonym/python-classversioning/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/fonganthonym/python-classversioning

.. |version| image:: https://img.shields.io/pypi/v/classversioning.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/classversioning

.. |wheel| image:: https://img.shields.io/pypi/wheel/classversioning.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/classversioning

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/classversioning.svg
    :alt: Supported versions
    :target: https://pypi.org/project/classversioning

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/classversioning.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/classversioning

.. |commits-since| image:: https://img.shields.io/github/commits-since/fonganthonym/python-classversioning/v0.3.0.svg
    :alt: Commits since latest release
    :target: https://github.com/fonganthonym/python-classversioning/compare/v0.3.0...master



.. end-badges

Extra objects for handling and typing HDF5 files.

* Free software: BSD 2-Clause License

Installation
============

::

    pip install classversioning

You can also install the in-development version with::

    pip install https://github.com/fonganthonym/python-classversioning/archive/master.zip


Documentation
=============


https://python-classversioning.readthedocs.io/


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
