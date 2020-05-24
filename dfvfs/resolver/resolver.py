# -*- coding: utf-8 -*-
"""The path specification resolver."""

from __future__ import unicode_literals

from dfvfs.credentials import keychain
from dfvfs.lib import definitions
from dfvfs.lib import errors
from dfvfs.mount import manager as mount_manager
from dfvfs.path import path_spec
from dfvfs.resolver import context


class Resolver(object):
  """Path specification resolver."""

  _resolver_context = context.Context()
  _resolver_helpers_manager = None

  key_chain = keychain.KeyChain()

  @classmethod
  def _GetResolverHelper(cls, type_indicator):
    """Retrieves the path specification resolver helper for the specified type.

    Args:
      type_indicator (str): type indicator.

    Returns:
      ResolverHelper: a resolver helper.
    """
    if not cls._resolver_helpers_manager:
      # Delay the import of the resolver helpers manager to prevent circular
      # imports.
      from dfvfs.resolver_helpers import manager  # pylint: disable=import-outside-toplevel

      cls._resolver_helpers_manager = manager.ResolverHelperManager

    return cls._resolver_helpers_manager.GetHelper(type_indicator)

  @classmethod
  def OpenFileEntry(cls, path_spec_object, resolver_context=None):
    """Opens a file entry object defined by path specification.

    Args:
      path_spec_object (PathSpec): path specification.
      resolver_context (Optional[Context]): resolver context, where None
          represents the built in context which is not multi process safe.

    Returns:
      FileEntry: file entry or None if the path specification could not be
          resolved.
    """
    file_system = cls.OpenFileSystem(
        path_spec_object, resolver_context=resolver_context)

    if resolver_context is None:
      resolver_context = cls._resolver_context

    file_entry = file_system.GetFileEntryByPathSpec(path_spec_object)

    # Release the file system so it will be removed from the cache
    # when the file entry is destroyed.
    resolver_context.ReleaseFileSystem(file_system)

    return file_entry

  @classmethod
  def OpenFileObject(cls, path_spec_object, resolver_context=None):
    """Opens a file-like object defined by path specification.

    Args:
      path_spec_object (PathSpec): path specification.
      resolver_context (Optional[Context]): resolver context, where None
          represents the built in context which is not multi process safe.

    Returns:
      FileIO: file-like object or None if the path specification could not
          be resolved.

    Raises:
      MountPointError: if the mount point specified in the path specification
          does not exist.
      PathSpecError: if the path specification is incorrect.
      TypeError: if the path specification type is unsupported.
    """
    if not isinstance(path_spec_object, path_spec.PathSpec):
      raise TypeError('Unsupported path specification type.')

    if resolver_context is None:
      resolver_context = cls._resolver_context

    if path_spec_object.type_indicator == definitions.TYPE_INDICATOR_MOUNT:
      if path_spec_object.HasParent():
        raise errors.PathSpecError(
            'Unsupported mount path specification with parent.')

      mount_point = getattr(path_spec_object, 'identifier', None)
      if not mount_point:
        raise errors.PathSpecError(
            'Unsupported path specification without mount point identifier.')

      path_spec_object = mount_manager.MountPointManager.GetMountPoint(
          mount_point)
      if not path_spec_object:
        raise errors.MountPointError(
            'No such mount point: {0:s}'.format(mount_point))

    file_object = resolver_context.GetFileObject(path_spec_object)
    if not file_object:
      resolver_helper = cls._GetResolverHelper(path_spec_object.type_indicator)
      file_object = resolver_helper.NewFileObject(resolver_context)

    file_object.open(path_spec=path_spec_object)
    return file_object

  @classmethod
  def OpenFileSystem(cls, path_spec_object, resolver_context=None):
    """Opens a file system object defined by path specification.

    Args:
      path_spec_object (PathSpec): path specification.
      resolver_context (Optional[Context]): resolver context, where None
          represents the built in context which is not multi process safe.

    Returns:
      FileSystem: file system or None if the path specification could not
          be resolved or has no file system object.

    Raises:
      AccessError: if the access to open the file system was denied.
      BackEndError: if the file system cannot be opened.
      MountPointError: if the mount point specified in the path specification
          does not exist.
      PathSpecError: if the path specification is incorrect.
      TypeError: if the path specification type is unsupported.
    """
    if not isinstance(path_spec_object, path_spec.PathSpec):
      raise TypeError('Unsupported path specification type.')

    if resolver_context is None:
      resolver_context = cls._resolver_context

    if path_spec_object.type_indicator == definitions.TYPE_INDICATOR_MOUNT:
      if path_spec_object.HasParent():
        raise errors.PathSpecError(
            'Unsupported mount path specification with parent.')

      mount_point = getattr(path_spec_object, 'identifier', None)
      if not mount_point:
        raise errors.PathSpecError(
            'Unsupported path specification without mount point identifier.')

      path_spec_object = mount_manager.MountPointManager.GetMountPoint(
          mount_point)
      if not path_spec_object:
        raise errors.MountPointError(
            'No such mount point: {0:s}'.format(mount_point))

    file_system = resolver_context.GetFileSystem(path_spec_object)
    if not file_system:
      resolver_helper = cls._GetResolverHelper(path_spec_object.type_indicator)
      file_system = resolver_helper.NewFileSystem(resolver_context)

    try:
      file_system.Open(path_spec_object)
    except (IOError, ValueError) as exception:
      raise errors.BackEndError(
          'Unable to open file system with error: {0!s}'.format(exception))

    return file_system
