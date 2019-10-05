Welcome to the Geocom Python Framework (GPF)
============================================

|python| |status| |pypi| |build| |issues| |docs|

.. |python| image:: https://img.shields.io/pypi/pyversions/gpf?logo=python
    :alt: Python version(s)

.. |status| image:: https://img.shields.io/pypi/status/gpf
    :alt: PyPI status

.. |pypi| image:: https://img.shields.io/pypi/v/gpf?logo=pypi
    :alt: PyPI homepage
    :target: https://pypi.org/project/gpf

.. |build| image:: https://img.shields.io/appveyor/ci/geonis-github/gpf?logo=appveyor
    :alt: AppVeyor
    :target: https://ci.appveyor.com/project/GEONIS-GITHUB/gpf

.. |issues| image:: https://img.shields.io/github/issues-raw/geocom-gis/gpf?logo=github
    :alt: GitHub issues
    :target: https://github.com/geocom-gis/gpf/issues

.. |docs| image:: https://img.shields.io/readthedocs/gpf?logo=read%20the%20docs
    :alt: Documentation
    :target: https://gpf.readthedocs.io/en/latest/

Purpose
-------

The *Geocom Python Framework* or ``gpf`` provides a set of Python modules that contain tools, helpers, loggers etc. for a more pleasant Python scripting experience in ArcGIS_ and/or GEONIS_.
GIS users who need to write geoprocessing scripts with ``arcpy`` might benefit from importing the ``gpf`` module into their script as well.

The ``gpf`` module in this repository has been developed for **Python 2.7.14+ (ArcGIS Desktop/Server)**.
However, it is also available for Python 3.6+ (ArcGIS Pro, Server) on `GitHub <https://github.com/geocom-gis/gpf3>`_ and `PyPI <https://pypi.org/project/gpf3>`_.

Geocom customers who need to write GEONIS menu or form scripts should also look into the ``gntools`` module on `GitHub <https://github.com/geocom-gis/gntools>`_ or `PyPI <https://pypi.org/project/gntools>`_.

.. _ArcGIS: https://www.esri.com
.. _GEONIS: https://geonis.com/en/solutions/framework/geonis

Requirements
------------

- ArcGIS Desktop and/or ArcGIS Server 10.6 or higher
- Python 2.7.14 or higher (along with the ``arcpy`` module)

Installation
------------

The easiest way to install the Geocom Python Framework, is to use pip_, a Python package manager.
When ``pip`` is installed, the user can simply run:

    ``python -m pip install gpf``

.. _pip: https://pip.pypa.io/en/stable/installing/

Documentation
-------------

The complete ``gpf`` documentation can be found at `Read the Docs`_.

.. _Read the Docs: https://gpf.readthedocs.io/

License
-------

`Apache License 2.0`_ © 2019 Geocom Informatik AG / VertiGIS & contributors

.. _Apache License 2.0: https://github.com/geocom-gis/gpf/blob/master/LICENSE
