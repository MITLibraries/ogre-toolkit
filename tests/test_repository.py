# -*- coding: utf-8 -*-
from __future__ import absolute_import
import unittest
import tempfile
import shutil
import os.path
import git
import io

from ogre.repository import Repository, Item


class RepositoryTestCase(unittest.TestCase):
    def setUp(self):
        self.remote_temp = tempfile.mkdtemp()
        self.local_temp = tempfile.mkdtemp()
        self.remote = os.path.join(self.remote_temp, 'repo')
        shutil.copytree('tests/fixtures/repo', self.remote)
        r = git.Repo.init(self.remote)
        r.index.add('*')
        r.index.commit('Nuke it from orbit')

    def tearDown(self):
        shutil.rmtree(self.remote_temp)
        shutil.rmtree(self.local_temp)

    def testCatalogReturnsDictionaryOfItems(self):
        repo = Repository(self.local_temp, self.remote)
        self.assertEqual(repo.catalog, {'foobar': 'foo/bar'})

    def testRepoReturnsItemsWhenIterated(self):
        repo = Repository(self.local_temp, self.remote)
        item = list(repo)[0]
        self.assertEqual(item.id, 'foobar')

    def testItemHasFileProperties(self):
        item = Item('fid', 'foo/bar/baz')
        self.assertEqual(item.fgdc, 'foo/bar/baz/fgdc.xml')

    def testUpdatePullsChangesFromRemote(self):
        repo = Repository(self.local_temp, self.remote)
        r = git.Repo(self.remote)
        r.index.commit('A new commit')
        repo.update()
        self.assertEqual(repo.repo.commit().message, 'A new commit')

    def testCommitCommitsChangesToLocal(self):
        repo = Repository(self.local_temp, self.remote)
        with io.open(os.path.join(self.local_temp, 'foo/bar/fgdc.xml'), 'wb') as fp:
            fp.write(u'foobar'.encode('utf-8'))
        repo.commit('Testing')
        self.assertEqual(repo.repo.commit().message, 'Testing')

    def testFindReturnsItemById(self):
        repo = Repository(self.local_temp, self.remote)
        item = repo.find('foobar')
        self.assertEqual(item.id, 'foobar')
