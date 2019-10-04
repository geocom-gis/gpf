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
Test modules for the :py:mod:``gpf`` package. Requires ``pytest``.
"""

import os
import sys

from gpf.common.const import ARCPY


class ArcPyMock(object):
    """
    Context manager that should be used before all test imports that depend on arcpy.
    If the environment variable specified by ArcPyMock.ENV_KEY is truthy,
    the arcpy module will be replaced by a MagicMock object.

    Note that arcpy is still unusable like this, but modules that depend on it can at least load properly.
    """

    ENV_KEY = 'mock_{}'.format(ARCPY)

    def __init__(self):
        pass

    def __enter__(self):
        if os.environ.get(ArcPyMock.ENV_KEY):
            from warnings import warn
            from mock import MagicMock

            sys.modules[ARCPY] = MagicMock()
            warn('The arcpy module has been replaced by a mock object ({} = true)'.format(ArcPyMock.ENV_KEY))

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return
