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

import os

import pytest

import gpf.paths as paths


def test_explode():
    assert paths.explode(r'C:/temp/test.gdb') == ('C:\\temp', 'test', '.gdb')
    assert paths.explode(r'C:/temp/folder') == ('C:\\temp', 'folder', '')


def test_normalize():
    assert paths.normalize(r'A/B\C') == 'a\\b\\c'
    assert paths.normalize(r'A/b\c', False) == 'A\\b\\c'


def test_join():
    assert paths.concat('a', 'b', 'c') == 'a\\b\\c'


def get_abs():
    curdir = os.path.dirname(__file__)
    assert paths.get_abs('test.txt') == os.path.join(curdir, 'test.txt')
    assert paths.get_abs('test.txt', os.path.dirname(curdir)) == os.path.join(os.path.dirname(curdir), 'test.txt')
    assert paths.get_abs(__file__) == os.path.normpath(__file__)


def test_pathmanager_bad_init():
    with pytest.raises(TypeError):
        paths.Path(None)
        paths.Path('')
    with pytest.raises(ValueError):
        paths.Path(r'C:\directory\file.ext', r'C:\directory')


def test_pathmanager_bad_file():
    pm = paths.Path(r'C:\directory\file.ext')
    assert not pm.is_file
    assert not pm.is_dir
    assert not pm.exists
    assert pm.extension() == '.ext'
    assert pm.extension(False) == 'ext'
    assert pm.basename() == 'file.ext'
    assert pm.basename(False) == 'file'
    assert pm.make_path('sub1', 'sub2') == 'C:\\directory\\sub1\\sub2\\file.ext'


def test_pathmanager_bad_dir():
    pm = paths.Path(r'C:\directory\test')
    assert not pm.is_file
    assert not pm.is_dir
    assert not pm.exists
    assert pm.extension() == ''
    assert pm.extension(False) == ''
    assert pm.basename() == 'test'
    assert pm.basename(False) == 'test'
    assert pm.make_path('sub1', 'sub2') == 'C:\\directory\\test\\sub1\\sub2'


def test_pathmanager_good_file():
    file_name = os.path.basename(__file__)
    dir_path = os.path.dirname(__file__)
    pm = paths.Path(__file__)
    assert pm.is_file
    assert not pm.is_dir
    assert pm.exists
    assert pm.extension() == '.py'
    assert pm.extension(False) == 'py'
    assert pm.basename() == file_name
    assert pm.basename(False) == file_name.split('.')[0]
    assert pm.make_path('sub1', 'sub2') == os.path.join(dir_path, 'sub1', 'sub2', file_name)


def test_pathmanager_good_dir():
    dir_path = os.path.dirname(__file__)
    dir_name = os.path.basename(dir_path)
    pm = paths.Path(dir_path)
    assert not pm.is_file
    assert pm.is_dir
    assert pm.exists
    assert pm.extension() == ''
    assert pm.extension(False) == ''
    assert pm.basename() == dir_name
    assert pm.basename(False) == dir_name
    assert pm.make_path('sub1', 'sub2') == os.path.join(dir_path, 'sub1', 'sub2')


def test_getworkspace():
    assert paths.get_workspace('C:\\temp\\test.gdb\\feature_dataset\\feature_class') == \
           paths.Workspace('C:\\temp\\test.gdb\\feature_dataset')
    assert paths.get_workspace(
            'C:\\temp\\test.gdb\\feature_dataset\\feature_class', True) == paths.Workspace('C:\\temp\\test.gdb')


def test_isgdbpath():
    assert paths.split_gdbpath('C:\\folder\\test.gdb\\q.fds\\q.fc') == ('C:\\folder\\test.gdb', 'fds', 'fc')
    assert paths.split_gdbpath('C:\\test.sde\\q.fds\\q.fc', False) == ('C:\\test.sde', 'q.fds', 'q.fc')
    with pytest.raises(ValueError):
        paths.split_gdbpath('C:\\test.gdb\\folder\\test2.gdb\\subfolder')
        paths.split_gdbpath('C:\\test.gdb\\a\\b\\c')


def test_wsmanager_gdb():
    wm = paths.Workspace('test.gdb', qualifier='TEST', base='C:\\temp', separator='|')
    assert wm.root == paths.Workspace('C:\\temp\\test.gdb')
    assert wm.qualifier == ''
    assert wm.separator == ''
    assert wm.make_path('ele', 'ele_kabel') == 'C:\\temp\\test.gdb\\ele\\ele_kabel'
    wm = paths.Workspace('C:\\temp\\test.gdb')
    assert not wm.exists
    assert wm.root == paths.Workspace('C:\\temp\\test.gdb')
    assert wm.get_parent(str(wm)) == 'C:\\temp\\test.gdb'
    assert wm.get_parent(str(wm), True) == 'C:\\temp'
    assert wm.get_root(str(wm)) == 'C:\\temp\\test.gdb'
    assert wm.is_gdb is True
    assert wm.qualifier == ''
    assert wm.separator == ''
    assert wm.qualify('test', 'my_qualifier') == 'test'
    with pytest.raises(ValueError):
        wm.qualify('')
    assert wm.make_path('ele', 'ele_kabel') == 'C:\\temp\\test.gdb\\ele\\ele_kabel'
    with pytest.raises(IndexError):
        wm.make_path('p1', 'p2', 'p3')
    assert paths.Workspace.get_root('C:\\temp\\test.shp') == 'C:\\temp'
    assert paths.Workspace.get_parent('C:\\temp\\test.shp') == 'C:\\temp'
    assert wm.get_root('C:\\temp\\test.gdb\\ele\\ele_kabel') == 'C:\\temp\\test.gdb'
