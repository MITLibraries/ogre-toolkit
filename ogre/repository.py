# -*- coding: utf-8 -*-
from __future__ import absolute_import
import fnmatch
import json
import io
import os
import os.path

import git


class FileProperty(object):
    def __init__(self, filename):
        self.filename = filename

    def __get__(self, instance, cls):
        fpath = os.path.join(instance.directory, self.filename)
        if os.path.isfile(fpath):
            return fpath


class Item(object):
    """
    An item in a repository.

    An ``Item`` provides access to the underlying metadata files for an
    item in a :class:`~ogre.repository.Repository`. Different files are
    accessed as properties that return a path to the file::

        from ogre.repository import Item

        item = Item('id_1', 'path/to/repo')
        item.id # 'id_1'
        item.fgdc # 'path/to/repo/id_1/fgdc.xml'

    Usually, items are obtained by iterating over a
    :class:`~ogre.repository.Repository` object.

    :param id: item id
    :param directory: directory of repository
    """

    fgdc = FileProperty('fgdc.xml')
    gbl_json = FileProperty('geoblacklight.json')

    def __init__(self, directory):
        self.directory = directory
        self._record = None

    @property
    def record(self):
        if self._record is None:
            with io.open(self.gbl_json) as fp:
                self._record = json.load(fp)
        return self._record


class Repository(object):
    """
    An object representing an OpenGeoMetadata repository.

    A ``Repository`` creates a local clone of a repo. If the local repo
    already exists, it will attempt to do a ``git pull``. It can be iterated
    over to produce :class:`~ogre.repository.Item`\s::

        from ogre.repository import Repository

        for item in Repository('path/to/local', 'path/to/remote'):
            print item.id

    :param path: path to local repo
    :param remote: path to remote repo to clone
    :param catalog_file: name of catalog file in repo
    """

    def __init__(self, directory, update=True):
        self.directory = directory
        self.repo = git.Repo(self.directory)
        if update:
            self.update()

    def __iter__(self):
        for root, dirs, files in os.walk(self.directory):
            for f in fnmatch.filter(files, 'geoblacklight.json'):
                yield Item(root)

    def update(self):
        """Perform ``git pull`` of repository."""
        self.repo.remotes.origin.pull()
