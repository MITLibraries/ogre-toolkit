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

    def testRepoReturnsItemsWhenIterated(self):
        repo = Repository(self.local_temp, self.remote)
        item = list(repo)[0]
        self.assertTrue(item.gbl_json.endswith('/foo/bar/geoblacklight.json'))

    def testItemHasFileProperties(self):
        item = Item('tests/fixtures/repo/foo/bar')
        self.assertEqual(item.fgdc, 'tests/fixtures/repo/foo/bar/fgdc.xml')

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
