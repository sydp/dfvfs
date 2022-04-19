# -*- coding: utf-8 -*-
"""The APFS directory implementation."""

from dfvfs.path import apfs_path_spec
from dfvfs.vfs import directory


class APFSDirectory(directory.Directory):
  """File system directory that uses pyfsapfs."""

  def __init__(self, file_system, path_spec, fsapfs_file_entry):
    """Initializes a directory.

    Args:
      file_system (FileSystem): file system.
      path_spec (PathSpec): path specification.
      fsapfs_file_entry (pyfsapfs.file_entry): APFS file entry.
    """
    super(APFSDirectory, self).__init__(file_system, path_spec)
    self._fsapfs_file_entry = fsapfs_file_entry

  def _EntriesGenerator(self):
    """Retrieves directory entries.

    Since a directory can contain a vast number of entries using
    a generator is more memory efficient.

    Yields:
      APFSPathSpec: APFS path specification.
    """
    location = getattr(self.path_spec, 'location', None)

    for fsapfs_sub_file_entry in self._fsapfs_file_entry.sub_file_entries:
      directory_entry = fsapfs_sub_file_entry.name

      if not location or location == self._file_system.PATH_SEPARATOR:
        directory_entry = self._file_system.JoinPath([directory_entry])
      else:
        directory_entry = self._file_system.JoinPath([
            location, directory_entry])

      yield apfs_path_spec.APFSPathSpec(
          identifier=fsapfs_sub_file_entry.identifier, location=directory_entry,
          parent=self.path_spec.parent)
