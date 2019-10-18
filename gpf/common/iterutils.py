# coding: utf-8

# Copyright (c) 2012 Erik Rose | MIT License

# Modifications:
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
This module only exists in the Python 2 version of the Geocom Python Framework (GPF). It contains functions from the
`more_itertools <https://github.com/erikrose/more-itertools/blob/master/more_itertools/more.py>`_ module
that are not available in the standard Python 2.7.14 library (ArcGIS 10.6 version).

To avoid dependencies in the GPF, these functions have been copied from their original source on GitHub and have been
slightly modified for better integration. The state of the functions listed below matches Git commit
`ec9e743 <https://github.com/erikrose/more-itertools/commit/ec9e743fe8b02db9acd04725abcde34998c4730b>`_.

.. warning::    This module should not be used in the Python 3 version of the Geocom Python Framework.
                It is recommended to use the built-in `more_itertools` module in this case.
"""

import gpf.common.const as _const
import gpf.common.validate as _vld


def collapse(iterable, base_type=None, levels=None):
    """
    Flatten an iterable with multiple levels of nesting (e.g., a list of
    lists of tuples) into non-iterable types.

        >>> iterable = [(1, 2), ([3, 4], [[5], [6]])]
        >>> list(collapse(iterable))
        [1, 2, 3, 4, 5, 6]

    String types are not considered iterable and will not be collapsed.
    To avoid collapsing other types, specify *base_type*:

        >>> iterable = ['ab', ('cd', 'ef'), ['gh', 'ij']]
        >>> list(collapse(iterable, base_type=tuple))
        ['ab', ('cd', 'ef'), 'gh', 'ij']

    Specify *levels* to stop flattening after a certain level:

    >>> iterable = [('a', ['b']), ('c', ['d'])]
    >>> list(collapse(iterable))  # Fully flattened
    ['a', 'b', 'c', 'd']
    >>> list(collapse(iterable, levels=1))  # Only one level flattened
    ['a', ['b'], 'c', ['d']]

    .. note::    Function copied from `more_itertools` package (Python 3 built-in).
    """

    def walk(node, level):
        if (
                ((levels is not None) and (level > levels)) or _vld.is_text(node) or
                ((base_type is not None) and isinstance(node, base_type))
        ):
            yield node
            return

        try:
            tree = iter(node)
        except TypeError:
            yield node
            return
        else:
            for child in tree:
                for v in walk(child, level + 1):
                    yield v

    for x in walk(iterable, 0):
        yield x


def first(iterable, default=_const.OBJ_EMPTY):
    """Return the first item of *iterable*, or *default* if *iterable* is
    empty.

        >>> first([0, 1, 2, 3])
        0
        >>> first([], 'some default')
        'some default'

    If *default* is not provided and there are no items in the iterable,
    raise ``ValueError``.

    :func:`first` is useful when you have a generator of expensive-to-retrieve
    values and want any arbitrary one. It is marginally shorter than
    ``next(iter(iterable), default)``.

    .. note::    Function copied from `more_itertools` package (Python 3 built-in).
    """
    try:
        return next(iter(iterable))
    except StopIteration:
        _vld.raise_if(default is _const.OBJ_EMPTY, ValueError,
                      'first() was called on an empty iterable, and no default value was provided.')
        return default
