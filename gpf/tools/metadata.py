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
The metadata module contains functions and classes that help describing data.
"""

import gpf.common.textutils as _tu
import gpf.cursors as _cursors
from gpf import arcpy as _arcpy

from warnings import warn as _warn


class DescribeWarning(RuntimeWarning):
    """ The warning type that is shown when ArcPy's :func:`Describe` failed. """
    pass


# noinspection PyPep8Naming
class Describe(object):
    """
    Wrapper class for the ArcPy ``Describe`` object.
    If ArcPy's :func:`Describe` failed, a warning will be shown but no errors will be (re)raised.
    Any ``Describe`` property that is retrieved, will return ``None`` in this case.

    If a property does not exist, it will return ``None``. If this is not desired,
    consider using the :func:`get` function, which behaves similar to a :func:`dict.get`.

    :param element:     The data element to describe.
    """

    _ATTR_FIELDS = 'fields'
    _ATTR_DATATYPE = 'dataType'
    _ATTR_OIDFIELD = 'OIDFieldName'
    _ATTR_SHPFIELD = 'shapeFieldName'
    _ATTR_LENFIELD = 'lengthFieldName'
    _ATTR_AREAFIELD = 'areaFieldName'
    _ATTR_RASTERFIELD = 'rasterFieldName'
    _ATTR_SUBTYPEFIELD = 'subtypeFieldName'
    _ATTR_GLOBALIDFIELD = 'globalIDFieldName'

    __slots__ = '_obj'

    def __init__(self, element):
        self._obj = None
        try:
            self._obj = _arcpy.Describe(element)
        except Exception as e:
            _warn(str(e), DescribeWarning)

    def __getattr__(self, name):
        """ Returns the property value of a Describe object item. """
        return self._get(name)

    def __contains__(self, item):
        """ Checks if a Describe object has the specified property. """
        return hasattr(self._obj, item)

    def __nonzero__(self):
        """ Checks if the Describe object is 'truthy' (i.e. not ``None``). """
        if self._obj:
            return True
        return False

    def _get(self, name):
        if not hasattr(self._obj, name) and name not in ('__dict__', '__members__', '__methods__'):
            _warn('Describe object of type {} does not have a {} attribute'.
                  format(_tu.to_repr(self.dataType), _tu.to_repr(name)), Warning)
            return None
        return getattr(self._obj, name)

    def get(self, name, default=None):
        """
        Returns the value of a ``Describe`` object attribute by *name*, returning *default* when it has not been found.
        This method does not show warnings or raise errors if the attribute does not exist.

        :param name:    The name of the property.
        :param default: The default value to return in case the property was not found.
        :type name:     str
        """
        return getattr(self._obj, name, default)

    def num_rows(self, where_clause=None):
        """
        Returns the number of rows in the table or feature class.

        If the current Describe object does not support this action or does not have any rows, 0 will be returned.

        :param where_clause:    An optional where clause to base the row count on.
        :type where_clause:     str, unicode, ~gpf.tools.queries.Where
        :rtype:                 int
        """
        field = None
        if where_clause:
            if isinstance(where_clause, basestring):
                field = _tu.unquote(where_clause.split()[0])
            elif hasattr(where_clause, 'fields'):
                field = where_clause.fields[0]
            else:
                raise ValueError('where_clause must be a string or Where instance')

        try:
            if field:
                # Iterate over the dataset rows, using the (first) field from the where_clause
                with _cursors.SearchCursor(self.catalogPath, field, where_clause=where_clause) as rows:
                    num_rows = sum(1 for _ in rows)
                del rows
            else:
                # Use the ArcPy GetCount() tool for the row count
                num_rows = int(_arcpy.GetCount_management(self.catalogPath).getOutput(0))
        except Exception as e:
            _warn(str(e), DescribeWarning)
            num_rows = 0

        return num_rows

    def get_fields(self, names_only=True, uppercase=False):
        """
        Returns a list of all fields in the described object (if any).

        :param names_only:  When ``True`` (default), a list of field names instead of ``Field`` instances is returned.
        :param uppercase:   When ``True`` (default=``False``), the returned field names will be uppercase.
                            This also applies when *names_only* is set to return ``Field`` instances.
        :type names_only:   bool
        :type uppercase:    bool
        :return:            List of field names or ``Field`` instances.
        :rtype:             list
        """
        if Describe._ATTR_FIELDS not in self:
            _warn('Describe object of type {} does not have a {} attribute'.
                  format(_tu.to_repr(self.dataType), _tu.to_repr(Describe._ATTR_FIELDS)), Warning)
            return []

        fields = [field.name if names_only else field for field in self._obj.fields]
        if uppercase:
            if names_only:
                return [field.upper() for field in fields]
            else:
                for f in fields:
                    f.name = f.name.upper()
        return fields

    def get_editable_fields(self, names_only=True, uppercase=False):
        """
        For data elements that have a *fields* property (e.g. Feature classes, Tables and workspaces),
        this will return a list of all editable (writable) fields.

        :param names_only:  When ``True`` (default), a list of field names instead of ``Field`` instances is returned.
        :param uppercase:   When ``True`` (default=``False``), the returned field names will be uppercase.
                            This also applies when *names_only* is set to return ``Field`` instances.
        :type names_only:   bool
        :type uppercase:    bool
        :return:            List of field names or ``Field`` instances.
        :rtype:             list
        """
        if Describe._ATTR_FIELDS not in self:
            _warn('Describe object of type {} does not have a {} attribute'.
                  format(_tu.to_repr(self.dataType), _tu.to_repr(Describe._ATTR_FIELDS)), Warning)
            return []

        return [field.name if names_only else field for field in self.fields(uppercase=uppercase) if field.editable]

    @property
    def dataType(self):
        """
        Returns the data type for this ``Describe`` object.
        All ``Describe`` objects should have this property.
        If it returns ``None``, the object has not been successfully retrieved.

        :rtype:     unicode
        """
        if not self:
            _warn('{} object is empty'.format(_tu.to_repr(Describe.__name__)), Warning)
            return None

        return self._obj.dataType

    @property
    def globalIDFieldName(self):
        """
        Global ID field name.
        Returns ``None`` if the field is missing or if the ``Describe`` object is not a dataset.

        :rtype: unicode
        """
        return self._get(Describe._ATTR_GLOBALIDFIELD)

    @property
    def OIDFieldName(self):
        """
        Object ID field name.
        Returns ``None`` if the field is missing or if the ``Describe`` object is not a dataset.

        :rtype: unicode
        """
        return self._get(Describe._ATTR_OIDFIELD)

    @property
    def shapeFieldName(self):
        """
        Perimeter or polyline length field name.
        Returns ``None`` if the field is missing or if the ``Describe`` object is not a dataset.

        :rtype: unicode
        """
        return self._get(Describe._ATTR_SHPFIELD)

    @property
    def lengthFieldName(self):
        """
        Perimeter or polyline length field name.
        Returns ``None`` if the field is missing or if the ``Describe`` object is not a dataset.

        :rtype: unicode
        """
        return self._get(Describe._ATTR_LENFIELD)

    @property
    def areaFieldName(self):
        """
        Polygon area field name.
        Returns ``None`` if the field is missing or if the ``Describe`` object is not a dataset.

        :rtype: unicode
        """
        return self._get(Describe._ATTR_AREAFIELD)

    @property
    def rasterFieldName(self):
        """
        Raster field name.
        Returns ``None`` if the field is missing or if the ``Describe`` object is not a dataset.

        :rtype: unicode
        """
        return self._get(Describe._ATTR_RASTERFIELD)

    @property
    def subtypeFieldName(self):
        """
        Subtype field name.
        Returns ``None`` if the field is missing or if the ``Describe`` object is not a dataset.

        :rtype: unicode
        """
        return self._get(Describe._ATTR_SUBTYPEFIELD)
