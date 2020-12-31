#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the TAR resolver helper implementation."""

import unittest

from dfvfs.resolver_helpers import tar_resolver_helper

from tests.resolver_helpers import test_lib


class TARResolverHelperTest(test_lib.ResolverHelperTestCase):
  """Tests for the TAR resolver helper implementation."""

  def testNewFileObject(self):
    """Tests the NewFileObject function."""
    resolver_helper_object = tar_resolver_helper.TARResolverHelper()
    self._TestNewFileObject(resolver_helper_object)

  def testNewFileSystem(self):
    """Tests the NewFileSystem function."""
    resolver_helper_object = tar_resolver_helper.TARResolverHelper()
    self._TestNewFileSystem(resolver_helper_object)


if __name__ == '__main__':
  unittest.main()
