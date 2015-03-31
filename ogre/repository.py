# -*- coding: utf-8 -*-
from __future__ import absolute_import
import io
import os.path
import json
import git


class FileProperty(object):
    def __init__(self, name, filename):
        self.name = name
        self.filename = filename

    def __get__(self, instance, cls):
        return os.path.join(instance.directory, self.filename)


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

    fgdc = FileProperty('fgdc', 'fgdc.xml')

    def __init__(self, id, directory):
        self.id = id
        self.directory = directory


def load_catalog(path):
    """
    Load the JSON catalog file.

    :param path: path to JSON catalog file
    """

    with io.open(path) as fp:
        return json.load(fp)


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

    def __init__(self, path, remote, catalog_file='layers.json'):
        self.directory = path
        try:
            self.repo = git.Repo(self.directory)
            self.update()
        except (git.exc.NoSuchPathError, git.exc.InvalidGitRepositoryError):
            self.repo = git.Repo.clone_from(remote, self.directory)
        #: Repository catalog in dictionary format
        self.catalog = load_catalog(os.path.join(self.directory, catalog_file))

    def __iter__(self):
        for id, subdirectory in self.catalog.items():
            yield Item(id, os.path.join(self.directory, subdirectory))

    def update(self):
        """Perform ``git pull`` of repository."""
        self.repo.remotes.origin.pull()

    def commit(self, message):
        """
        Perform ``git commit`` of repository.

        :param message: commit message
        """

        self.repo.index.commit(message)

    def find(self, id):
        """Find an :class:`~ogre.repository.Item` in the repository by id."""
        return Item(id, self.catalog[id])
