Welcome to the Geocom Python Framework (GPF)
============================================

|docs|

.. |docs| image:: https://readthedocs.org/projects/gpf/badge/
    :alt: Documentation Status
    :scale: 100%
    :target: https://gpf.readthedocs.io/en/latest/

Purpose
-------

The *Geocom Python Framework* or `gpf` provides a set of Python modules that contain tools, helpers, loggers etc. for a more pleasant Python scripting experience in ArcGIS_ and/or GEONIS_.
GIS users who need to write geoprocessing scripts with `arcpy` might benefit from importing the `gpf` module into their script as well.

The `gpf` module in this repository has been developed for **Python 2.7.14+ (ArcGIS Desktop/Server)**.
However, it is `also available for Python 3.6+`_ (ArcGIS Pro, Server).

Geocom customers who need to write GEONIS menu or form scripts should also look into the `gntools`_ module.

.. _ArcGIS: https://www.esri.com
.. _GEONIS: https://geonis.com/en/solutions/framework/geonis
.. _also available for Python 3.6+: https://pypi.org/project/gpf3
.. _gntools: https://pypi.org/project/gntools

Requirements
------------

- ArcGIS Desktop and/or ArcGIS Server 10.6 or higher
- Python 2.7.14 or higher (along with the `arcpy` module)

Installation
------------

The easiest way to install the Geocom Python Framework, is to use `pip`_, a Python package manager.
When `pip` is installed, the user can simply run:

    ``python -m pip install gpf``

.. _pip: https://pip.pypa.io/en/stable/installing/

Documentation
-------------

The complete `gpf` documentation can be found at `Read the Docs`_.

.. _Read the Docs: https://gpf.readthedocs.io/

License
-------

`Apache License 2.0`_ © 2019 Geocom Informatik AG / VertiGIS & contributors

.. _Apache License 2.0: https://github.com/geocom-gis/gpf/blob/master/LICENSE
