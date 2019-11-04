# coding: utf-8
#
# Copyright 2019 Geocom Informatik AG / VertiGIS

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This is the documentation for the **gpf** (*Geocom Python Framework*) package for **Python 2.7**.
For the Python 3 version (suitable for ArcGIS Pro), please refer to the **gpf3** package.

The *gpf* package contains several subpackages with tools and helpers for all kinds of
ArcGIS-related geoprocessing and data management tasks.
It is released under the Apache License 2.0 as an open-source product,
allowing the community to freely use it, improve it and possibly add new features.

Several tools in this package require Esri's ``arcpy`` Python library, which does not make this a *free* package.
However, users who have already installed and authorized ArcGIS Desktop (ArcMap, ArcCatalog etc.) should be able to work
with this package without any problems.

.. note::   It is recommended to import ``arcpy`` via the ``gpf`` package (``from gpf import arcpy``).
            This will load the same (and unmodified) module as ``import arcpy`` would load, but it shows
            more useful error messages when the import fails.
"""

import sys as _sys

from gpf.common import const as _const

_NOT_INITIALIZED = 'NotInitialized'


try:
    # Import the arcpy module globally
    import arcpy
except RuntimeError as e:
    if _NOT_INITIALIZED in str(e):
        # If the rather obscure "RuntimeError: NotInitialized" error is thrown,
        # raise an ImportError instead with a clear reason.
        raise ImportError('Failed to obtain an ArcGIS license for the {!r} module'.format(_const.PYMOD_ARCPY))
    # Reraise for all other RuntimeErrors
    raise
except ImportError:
    if _const.PYMOD_ARCPY not in _sys.modules:
        # If arcpy cannot be found in the system modules,
        # raise an ImportError that tells the user which interpreter is being used.
        # The user might have accidentally chosen a "vanilla" Python interpreter,
        # instead of the ArcGIS Python distribution.
        raise ImportError('Python interpreter at {!r} '
                          'cannot find the {!r} module'.format(_sys.executable, _const.PYMOD_ARCPY))
    # Reraise for other (unlikely) ImportErrors
    raise
