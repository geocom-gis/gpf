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
The *tools* subpackage contains a set of general classes and functions that
should make it a little easier to work with ArcGIS and ``arcpy``.

Some classes are wrappers for well-known ``arcpy`` classes,
created for a more user-friendly experience and/or better performance.
"""

import sys as _sys

import gpf.common.const as _const

_NOT_INITIALIZED = 'NotInitialized'


try:
    # Import the arcpy module globally
    import arcpy
except RuntimeError as e:
    if _NOT_INITIALIZED in str(e):
        # If the rather obscure "RuntimeError: NotInitialized" error is thrown,
        # raise an ImportError instead with a clear reason.
        raise ImportError('Failed to obtain an ArcGIS license for the {!r} module'.format(_const.ARCPY))
    # Reraise for all other RuntimeErrors
    raise
except ImportError:
    if _const.ARCPY not in _sys.modules:
        # If arcpy cannot be found in the system modules,
        # raise an ImportError that tells the user which interpreter is being used.
        # The user might have accidentally chosen a "vanilla" Python interpreter,
        # instead of the ArcGIS Python distribution.
        raise ImportError('Python interpreter at {!r} '
                          'cannot find the {!r} module'.format(_sys.executable, _const.ARCPY))
    # Reraise for other (unlikely) ImportErrors
    raise
