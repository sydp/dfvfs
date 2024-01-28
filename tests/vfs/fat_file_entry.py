#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the file entry implementation using pyfsfat."""

import unittest

from dfvfs.lib import definitions
from dfvfs.path import factory as path_spec_factory
from dfvfs.resolver import context
from dfvfs.vfs import fat_file_entry
from dfvfs.vfs import fat_file_system

from tests import test_lib as shared_test_lib


class FATFileEntryTest(shared_test_lib.BaseTestCase):
  """Tests the FAT file entry."""

  # pylint: disable=protected-access

  _IDENTIFIER_A_DIRECTORY = 0x1a40
  _IDENTIFIER_A_FILE = 0x6260
  _IDENTIFIER_ANOTHER_FILE = 0x62a0

  def setUp(self):
    """Sets up the needed objects used throughout the test."""
    self._resolver_context = context.Context()
    test_path = self._GetTestFilePath(['fat12.raw'])
    self._SkipIfPathNotExists(test_path)

    test_os_path_spec = path_spec_factory.Factory.NewPathSpec(
        definitions.TYPE_INDICATOR_OS, location=test_path)
    self._raw_path_spec = path_spec_factory.Factory.NewPathSpec(
        definitions.TYPE_INDICATOR_RAW, parent=test_os_path_spec)
    self._fat_path_spec = path_spec_factory.Factory.NewPathSpec(
        definitions.TYPE_INDICATOR_FAT, location='\\',
        parent=self._raw_path_spec)

    self._file_system = fat_file_system.FATFileSystem(
        self._resolver_context, self._fat_path_spec)
    self._file_system.Open()

  def tearDown(self):
    """Cleans up the needed objects used throughout the test."""
    self._resolver_context.Empty()

  def testInitialize(self):
    """Tests the __init__ function."""
    file_entry = fat_file_entry.FATFileEntry(
        self._resolver_context, self._file_system, self._fat_path_spec)

    self.assertIsNotNone(file_entry)

  def testGetDataStreams(self):
    """Tests the _GetDataStreams function."""
    path_spec = path_spec_factory.Factory.NewPathSpec(
        definitions.TYPE_INDICATOR_FAT,
        identifier=self._IDENTIFIER_ANOTHER_FILE,
        location='\\a_directory\\another_file',
        parent=self._raw_path_spec)
    file_entry = self._file_system.GetFileEntryByPathSpec(path_spec)
    self.assertIsNotNone(file_entry)

    data_streams = file_entry._GetDataStreams()
    self.assertEqual(len(data_streams), 1)

  def testGetStatAttribute(self):
    """Tests the _GetStatAttribute function."""
    path_spec = path_spec_factory.Factory.NewPathSpec(
        definitions.TYPE_INDICATOR_FAT,
        identifier=self._IDENTIFIER_ANOTHER_FILE,
        location='\\a_directory\\another_file',
        parent=self._raw_path_spec)
    file_entry = self._file_system.GetFileEntryByPathSpec(path_spec)
    self.assertIsNotNone(file_entry)

    stat_attribute = file_entry._GetStatAttribute()

    self.assertIsNotNone(stat_attribute)
    self.assertIsNone(stat_attribute.group_identifier)
    self.assertEqual(stat_attribute.inode_number, 0x62a0)
    self.assertIsNone(stat_attribute.mode)
    self.assertIsNone(stat_attribute.number_of_links)
    self.assertIsNone(stat_attribute.owner_identifier)
    self.assertEqual(stat_attribute.size, 22)
    self.assertEqual(stat_attribute.type, stat_attribute.TYPE_FILE)

  def testAccessTime(self):
    """Test the access_time property."""
    path_spec = path_spec_factory.Factory.NewPathSpec(
        definitions.TYPE_INDICATOR_FAT,
        identifier=self._IDENTIFIER_ANOTHER_FILE,
        location='\\a_directory\\another_file',
        parent=self._raw_path_spec)
    file_entry = self._file_system.GetFileEntryByPathSpec(path_spec)

    self.assertIsNotNone(file_entry)
    self.assertIsNotNone(file_entry.access_time)

  def testCreationTime(self):
    """Test the creation_time property."""
    path_spec = path_spec_factory.Factory.NewPathSpec(
        definitions.TYPE_INDICATOR_FAT,
        identifier=self._IDENTIFIER_ANOTHER_FILE,
        location='\\a_directory\\another_file',
        parent=self._raw_path_spec)
    file_entry = self._file_system.GetFileEntryByPathSpec(path_spec)

    self.assertIsNotNone(file_entry)
    self.assertIsNotNone(file_entry.creation_time)

  def testDataStreams(self):
    """Tests the data_streams property."""
    path_spec = path_spec_factory.Factory.NewPathSpec(
        definitions.TYPE_INDICATOR_FAT,
        identifier=self._IDENTIFIER_ANOTHER_FILE,
        location='\\a_directory\\another_file',
        parent=self._raw_path_spec)
    file_entry = self._file_system.GetFileEntryByPathSpec(path_spec)
    self.assertIsNotNone(file_entry)

    self.assertEqual(file_entry.number_of_data_streams, 1)

    data_stream_names = []
    for data_stream in file_entry.data_streams:
      data_stream_names.append(data_stream.name)

    self.assertEqual(data_stream_names, [''])

    path_spec = path_spec_factory.Factory.NewPathSpec(
        definitions.TYPE_INDICATOR_FAT, identifier=self._IDENTIFIER_A_DIRECTORY,
        location='\\a_directory', parent=self._raw_path_spec)
    file_entry = self._file_system.GetFileEntryByPathSpec(path_spec)
    self.assertIsNotNone(file_entry)

    self.assertEqual(file_entry.number_of_data_streams, 0)

    data_stream_names = []
    for data_stream in file_entry.data_streams:
      data_stream_names.append(data_stream.name)

    self.assertEqual(data_stream_names, [])

  def testModificationTime(self):
    """Test the modification_time property."""
    path_spec = path_spec_factory.Factory.NewPathSpec(
        definitions.TYPE_INDICATOR_FAT,
        identifier=self._IDENTIFIER_ANOTHER_FILE,
        location='\\a_directory\\another_file',
        parent=self._raw_path_spec)
    file_entry = self._file_system.GetFileEntryByPathSpec(path_spec)

    self.assertIsNotNone(file_entry)
    self.assertIsNotNone(file_entry.modification_time)

  def testSize(self):
    """Test the size property."""
    path_spec = path_spec_factory.Factory.NewPathSpec(
        definitions.TYPE_INDICATOR_FAT,
        identifier=self._IDENTIFIER_ANOTHER_FILE,
        location='\\a_directory\\another_file',
        parent=self._raw_path_spec)
    file_entry = self._file_system.GetFileEntryByPathSpec(path_spec)

    self.assertIsNotNone(file_entry)
    self.assertEqual(file_entry.size, 22)

  def testSubFileEntries(self):
    """Tests the number_of_sub_file_entries and sub_file_entries properties."""
    path_spec = path_spec_factory.Factory.NewPathSpec(
        definitions.TYPE_INDICATOR_FAT, location='\\',
        parent=self._raw_path_spec)
    file_entry = self._file_system.GetFileEntryByPathSpec(path_spec)
    self.assertIsNotNone(file_entry)

    self.assertEqual(file_entry.number_of_sub_file_entries, 2)

    expected_sub_file_entry_names = [
        'a_directory',
        'passwords.txt']

    sub_file_entry_names = []
    for sub_file_entry in file_entry.sub_file_entries:
      sub_file_entry_names.append(sub_file_entry.name)

    self.assertEqual(
        len(sub_file_entry_names), len(expected_sub_file_entry_names))
    self.assertEqual(
        sorted(sub_file_entry_names), sorted(expected_sub_file_entry_names))

    # Test a path specification without a location.
    path_spec = path_spec_factory.Factory.NewPathSpec(
        definitions.TYPE_INDICATOR_FAT, identifier=self._IDENTIFIER_A_DIRECTORY,
        parent=self._raw_path_spec)
    file_entry = self._file_system.GetFileEntryByPathSpec(path_spec)
    self.assertIsNotNone(file_entry)

    self.assertEqual(file_entry.number_of_sub_file_entries, 2)

  def testGetDataStream(self):
    """Tests the GetDataStream function."""
    path_spec = path_spec_factory.Factory.NewPathSpec(
        definitions.TYPE_INDICATOR_FAT,
        identifier=self._IDENTIFIER_ANOTHER_FILE,
        location='\\a_directory\\another_file',
        parent=self._raw_path_spec)
    file_entry = self._file_system.GetFileEntryByPathSpec(path_spec)
    self.assertIsNotNone(file_entry)

    data_stream = file_entry.GetDataStream('')
    self.assertIsNotNone(data_stream)

  def testGetExtents(self):
    """Tests the GetExtents function."""
    path_spec = path_spec_factory.Factory.NewPathSpec(
        definitions.TYPE_INDICATOR_FAT,
        identifier=self._IDENTIFIER_ANOTHER_FILE,
        location='\\a_directory\\another_file',
        parent=self._raw_path_spec)
    file_entry = self._file_system.GetFileEntryByPathSpec(path_spec)
    self.assertIsNotNone(file_entry)

    extents = file_entry.GetExtents()
    self.assertEqual(len(extents), 1)

    self.assertEqual(extents[0].extent_type, definitions.EXTENT_TYPE_DATA)
    self.assertEqual(extents[0].offset, 31232)
    self.assertEqual(extents[0].size, 2048)

    path_spec = path_spec_factory.Factory.NewPathSpec(
        definitions.TYPE_INDICATOR_FAT, identifier=self._IDENTIFIER_A_DIRECTORY,
        location='\\a_directory', parent=self._raw_path_spec)
    file_entry = self._file_system.GetFileEntryByPathSpec(path_spec)
    self.assertIsNotNone(file_entry)

    extents = file_entry.GetExtents()
    self.assertEqual(len(extents), 0)

  def testGetFileEntryByPathSpec(self):
    """Tests the GetFileEntryByPathSpec function."""
    path_spec = path_spec_factory.Factory.NewPathSpec(
        definitions.TYPE_INDICATOR_FAT, identifier=self._IDENTIFIER_A_FILE,
        parent=self._raw_path_spec)
    file_entry = self._file_system.GetFileEntryByPathSpec(path_spec)

    self.assertIsNotNone(file_entry)

  def testGetFileObject(self):
    """Tests the GetFileObject function."""
    path_spec = path_spec_factory.Factory.NewPathSpec(
        definitions.TYPE_INDICATOR_FAT,
        identifier=self._IDENTIFIER_ANOTHER_FILE,
        location='\\a_directory\\another_file',
        parent=self._raw_path_spec)
    file_entry = self._file_system.GetFileEntryByPathSpec(path_spec)
    self.assertIsNotNone(file_entry)

    file_object = file_entry.GetFileObject()
    self.assertIsNotNone(file_object)

    self.assertEqual(file_object.get_size(), 22)

    file_object = file_entry.GetFileObject(data_stream_name='bogus')
    self.assertIsNone(file_object)

    path_spec = path_spec_factory.Factory.NewPathSpec(
        definitions.TYPE_INDICATOR_FAT, identifier=self._IDENTIFIER_A_DIRECTORY,
        location='\\a_directory', parent=self._raw_path_spec)
    file_entry = self._file_system.GetFileEntryByPathSpec(path_spec)
    self.assertIsNotNone(file_entry)

    file_object = file_entry.GetFileObject()
    self.assertIsNone(file_object)

  def testGetParentFileEntry(self):
    """Tests the GetParentFileEntry function."""
    path_spec = path_spec_factory.Factory.NewPathSpec(
        definitions.TYPE_INDICATOR_FAT,
        identifier=self._IDENTIFIER_ANOTHER_FILE,
        location='\\a_directory\\another_file',
        parent=self._raw_path_spec)
    file_entry = self._file_system.GetFileEntryByPathSpec(path_spec)
    self.assertIsNotNone(file_entry)

    parent_file_entry = file_entry.GetParentFileEntry()

    self.assertIsNotNone(parent_file_entry)

    self.assertEqual(parent_file_entry.name, 'a_directory')

  def testIsFunctions(self):
    """Tests the Is* functions."""
    path_spec = path_spec_factory.Factory.NewPathSpec(
        definitions.TYPE_INDICATOR_FAT,
        identifier=self._IDENTIFIER_ANOTHER_FILE,
        location='\\a_directory\\another_file',
        parent=self._raw_path_spec)
    file_entry = self._file_system.GetFileEntryByPathSpec(path_spec)
    self.assertIsNotNone(file_entry)

    self.assertFalse(file_entry.IsRoot())
    self.assertFalse(file_entry.IsVirtual())
    self.assertTrue(file_entry.IsAllocated())

    self.assertFalse(file_entry.IsDevice())
    self.assertFalse(file_entry.IsDirectory())
    self.assertTrue(file_entry.IsFile())
    self.assertFalse(file_entry.IsLink())
    self.assertFalse(file_entry.IsPipe())
    self.assertFalse(file_entry.IsSocket())

    path_spec = path_spec_factory.Factory.NewPathSpec(
        definitions.TYPE_INDICATOR_FAT, identifier=self._IDENTIFIER_A_DIRECTORY,
        location='\\a_directory', parent=self._raw_path_spec)
    file_entry = self._file_system.GetFileEntryByPathSpec(path_spec)
    self.assertIsNotNone(file_entry)

    self.assertFalse(file_entry.IsRoot())
    self.assertFalse(file_entry.IsVirtual())
    self.assertTrue(file_entry.IsAllocated())

    self.assertFalse(file_entry.IsDevice())
    self.assertTrue(file_entry.IsDirectory())
    self.assertFalse(file_entry.IsFile())
    self.assertFalse(file_entry.IsLink())
    self.assertFalse(file_entry.IsPipe())
    self.assertFalse(file_entry.IsSocket())

    path_spec = path_spec_factory.Factory.NewPathSpec(
        definitions.TYPE_INDICATOR_FAT, location='\\',
        parent=self._raw_path_spec)
    file_entry = self._file_system.GetFileEntryByPathSpec(path_spec)
    self.assertIsNotNone(file_entry)

    self.assertTrue(file_entry.IsRoot())
    self.assertFalse(file_entry.IsVirtual())
    self.assertTrue(file_entry.IsAllocated())

    self.assertFalse(file_entry.IsDevice())
    self.assertTrue(file_entry.IsDirectory())
    self.assertFalse(file_entry.IsFile())
    self.assertFalse(file_entry.IsLink())
    self.assertFalse(file_entry.IsPipe())
    self.assertFalse(file_entry.IsSocket())


if __name__ == '__main__':
  unittest.main()
