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
The metadata module contains functions and classes that help describe data.
"""

from warnings import warn as _warn

import gpf.common.const as _const
import gpf.common.textutils as _tu
import gpf.cursors as _cursors
import gpf.tools.fieldutils as _fu
from gpf import arcpy as _arcpy


class DescribeWarning(RuntimeWarning):
    """ The warning type that is shown when ArcPy's :func:`arcpy.Describe` failed. """
    pass


# noinspection PyPep8Naming
class Describe(object):
    """
    Wrapper class for the ArcPy ``Describe`` object that exposes the most commonly used properties.

    If ArcPy's :func:`arcpy.Describe` failed, a warning will be shown but no errors will be (re)raised.
    Any ``Describe`` property that is retrieved, will return ``None`` in this case.

    If a property does not exist, it will also return ``None``. If this is not desired,
    consider using the :func:`get` function, which behaves similar to a :func:`dict.get`
    and can return a user-defined default value if the property was not found.

    **Params:**

    -   **element** (object):

        An object, name, or path of an element for which to retrieve its metadata.

    .. note::   Only a limited amount of properties has been exposed in this class.
                For a complete list of all possible properties, please have a look `here`_.
                For these unlisted properties, the same rule applies: if it doesn't exist,
                ``None`` is returned. If another return value is required, use :func:`get`.

    .. _here:   https://desktop.arcgis.com/en/arcmap/latest/analyze/arcpy-functions/describe-object-properties.htm
    """

    # Exposed properties
    _ATTR_FIELDS = 'fields'
    _ATTR_INDEXES = 'indexes'
    _ATTR_DATATYPE = 'dataType'
    _ATTR_SHAPETYPE = 'shapeType'
    _ATTR_DATASETTYPE = 'datasetType'
    _ATTR_ZAWARE = 'hasZ'
    _ATTR_MAWARE = 'hasM'
    _ATTR_EXTENT = 'extent'
    _ATTR_SPATREF = 'spatialReference'
    _ATTR_VERSIONED = 'isVersioned'

    __slots__ = '_obj'

    def __init__(self, element):
        self._obj = None
        try:
            self._obj = _arcpy.Describe(element)
        except Exception as e:
            _warn(str(e), DescribeWarning)

    def __getattr__(self, name):
        """ Returns the property value of a Describe object item. """
        return self.get(name)

    def __contains__(self, item):
        """ Checks if a Describe object has the specified property. """
        return hasattr(self._obj, item)

    def __nonzero__(self):
        """ Checks if the Describe object is 'truthy' (i.e. not ``None``). """
        if self._obj:
            return True
        return False

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
        Returns the number of rows for a table or feature class.

        If the current ``Describe`` object does not support this action or does not have any rows, 0 will be returned.

        :param where_clause:    An optional where clause to base the row count on.
        :type where_clause:     str, unicode, gpf.tools.queries.Where
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

    @property
    def dataType(self):
        """
        Returns the data type for this ``Describe`` object.
        All ``Describe`` objects should have this property.
        If it returns ``None``, the object has not been successfully retrieved.

        :rtype: unicode
        """
        if not self:
            return None

        return self._obj.dataType

    @property
    def datasetType(self):
        """
        Returns the name of the dataset type (e.g. Table, FeatureClass etc.).
        If the described object is not a dataset, ``None`` is returned.

        :rtype: unicode
        """
        return self.get(Describe._ATTR_DATASETTYPE)

    @property
    def shapeType(self):
        """
        Returns the geometry type for this ``Describe`` object.
        This will return 'Polygon', 'Polyline', 'Point', 'Multipoint' or 'MultiPatch'
        if the described object is a feature class, or ``None`` if it's not.

        :rtype: unicode
        """
        return self.get(Describe._ATTR_SHAPETYPE)

    @property
    def fields(self):
        """
        Returns a list of all ``Field`` objects (attributes) for this ``Describe`` object.
        If the described object is not a dataset, this will return an empty list.

        :rtype: list
        """
        return self.get(Describe._ATTR_FIELDS) or []

    @property
    def indexes(self):
        """
        Returns a list of all ``Index`` objects (attribute indexes) for this ``Describe`` object.
        If the described object is not a dataset, this will return an empty list.

        :rtype: list
        """
        return self.get(Describe._ATTR_INDEXES) or []

    def get_fields(self, names_only=True, uppercase=False):
        """
        Returns a list of all fields in the described object (if any).

        :param names_only:  When ``True`` (default), a list of field *names* instead of ``Field`` instances is returned.
        :param uppercase:   When ``True`` (default=``False``), the returned field names will be uppercase.
                            This also applies when *names_only* is set to return ``Field`` instances.
        :type names_only:   bool
        :type uppercase:    bool
        :return:            List of field names or ``Field`` instances.
        :rtype:             list
        """
        return _fu.list_fields(self.fields, names_only, uppercase)

    def get_editable_fields(self, names_only=True, uppercase=False):
        """
        For data elements that have a *fields* property (e.g. Feature classes, Tables and workspaces),
        this will return a list of all editable (writable) fields.

        :param names_only:  When ``True`` (default), a list of field *names* instead of ``Field`` instances is returned.
        :param uppercase:   When ``True`` (default=``False``), the returned field names will be uppercase.
                            This also applies when *names_only* is set to return ``Field`` instances.
        :type names_only:   bool
        :type uppercase:    bool
        :return:            List of field names or ``Field`` instances.
        :rtype:             list
        """
        return [field.name if names_only else field for field in self.get_fields(uppercase=uppercase) if field.editable]

    @property
    def extent(self):
        """
        Returns an ``Extent`` object for this ``Describe`` element.
        If the described object is not a feature class, this will return an empty ``Extent``.

        :rtype: arcpy.Extent
        """
        return self.get(Describe._ATTR_EXTENT) or _arcpy.Extent()

    @property
    def spatialReference(self):
        """
        Returns a ``SpatialReference`` object for this ``Describe`` element.
        If the described object is not a feature class, this will return an empty ``SpatialReference``.

        :rtype: arcpy.SpatialReference
        """
        return self.get(Describe._ATTR_SPATREF) or _arcpy.SpatialReference()

    @property
    def isVersioned(self):
        """
        Returns ``True`` if the ``Describe`` element refers to a versioned dataset.
        If the described object is not a dataset or not versioned, this will return ``False``.

        :rtype: bool
        """
        return self.get(Describe._ATTR_VERSIONED) or False

    @property
    def is_pointclass(self):
        """
        Returns ``True`` if the described object is a Point feature class.

        :rtype: bool
        """
        return self.get(Describe._ATTR_SHAPETYPE) == _const.SHP_POINT

    @property
    def is_multipointclass(self):
        """
        Returns ``True`` if the described object is a Multipoint feature class.

        :rtype: bool
        """
        return self.get(Describe._ATTR_SHAPETYPE) == _const.SHP_MULTIPOINT

    @property
    def is_polylineclass(self):
        """
        Returns ``True`` if the described object is a Polyline feature class.

        :rtype: bool
        """
        return self.get(Describe._ATTR_SHAPETYPE) == _const.SHP_POLYLINE

    @property
    def is_polygonclass(self):
        """
        Returns ``True`` if the described object is a Polygon feature class.

        :rtype: bool
        """
        return self.get(Describe._ATTR_SHAPETYPE) == _const.SHP_POLYGON

    @property
    def is_multipatchclass(self):
        """
        Returns ``True`` if the described object is a MultiPatch feature class.

        :rtype: bool
        """
        return self.get(Describe._ATTR_SHAPETYPE) == _const.SHP_MULTIPATCH

    @property
    def is_featureclass(self):
        """
        Returns ``True`` if the described object is a feature class.

        :rtype: bool
        """
        return self.get(Describe._ATTR_DATASETTYPE) == _const.DESC_TYPE_FEATURECLASS

    @property
    def is_featuredataset(self):
        """
        Returns ``True`` if the described object is a feature dataset.

        :rtype: bool
        """
        return self.get(Describe._ATTR_DATASETTYPE) == _const.DESC_TYPE_FEATUREDATASET

    @property
    def is_geometricnetwork(self):
        """
        Returns ``True`` if the described object is a geometric network.

        :rtype: bool
        """
        return self.get(Describe._ATTR_DATASETTYPE) == _const.DESC_TYPE_GEOMETRICNET

    @property
    def is_mosaicdataset(self):
        """
        Returns ``True`` if the described object is a mosaic dataset (raster).

        :rtype: bool
        """
        return self.get(Describe._ATTR_DATASETTYPE) == _const.DESC_TYPE_MOSAICRASTER

    @property
    def is_rasterdataset(self):
        """
        Returns ``True`` if the described object is a raster dataset.

        :rtype: bool
        """
        return self.get(Describe._ATTR_DATASETTYPE) == _const.DESC_TYPE_RASTER

    @property
    def is_table(self):
        """
        Returns ``True`` if the described object is a table.

        :rtype: bool
        """
        return self.get(Describe._ATTR_DATASETTYPE) == _const.DESC_TYPE_TABLE

    @property
    def hasZ(self):
        """
        Returns ``True`` if the described object is Z aware (i.e. is 3D).
        If the object is not a feature class or not Z aware, ``False`` is returned.

        :rtype: bool
        """
        return self.get(Describe._ATTR_ZAWARE) or False

    @property
    def hasM(self):
        """
        Returns ``True`` if the described object is M aware (i.e. has measures).
        If the object is not a feature class or not M aware, ``False`` is returned.

        :rtype: bool
        """
        return self.get(Describe._ATTR_MAWARE) or False

    @property
    def globalIDFieldName(self):
        """
        Global ID field name.
        Returns ``None`` if the field is missing or if the ``Describe`` object is not a dataset.

        :rtype: unicode
        """
        return self.get(_const.DESC_FIELD_GLOBALID)

    @property
    def OIDFieldName(self):
        """
        Object ID field name.
        Returns ``None`` if the field is missing or if the ``Describe`` object is not a dataset.

        :rtype: unicode
        """
        return self.get(_const.DESC_FIELD_OID)

    @property
    def shapeFieldName(self):
        """
        Perimeter or polyline length field name.
        Returns ``None`` if the field is missing or if the ``Describe`` object is not a dataset.

        :rtype: unicode
        """
        return self.get(_const.DESC_FIELD_SHAPE)

    @property
    def lengthFieldName(self):
        """
        Perimeter or polyline length field name.
        Returns ``None`` if the field is missing or if the ``Describe`` object is not a dataset.

        :rtype: unicode
        """
        return self.get(_const.DESC_FIELD_LENGTH)

    @property
    def areaFieldName(self):
        """
        Polygon area field name.
        Returns ``None`` if the field is missing or if the ``Describe`` object is not a dataset.

        :rtype: unicode
        """
        return self.get(_const.DESC_FIELD_AREA)

    @property
    def rasterFieldName(self):
        """
        Raster field name.
        Returns ``None`` if the field is missing or if the ``Describe`` object is not a dataset.

        :rtype: unicode
        """
        return self.get(_const.DESC_FIELD_RASTER)

    @property
    def subtypeFieldName(self):
        """
        Subtype field name.
        Returns ``None`` if the field is missing or if the ``Describe`` object is not a dataset.

        :rtype: unicode
        """
        return self.get(_const.DESC_FIELD_SUBTYPE)
