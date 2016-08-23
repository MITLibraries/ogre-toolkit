# -*- coding: utf-8 -*-
from __future__ import absolute_import
import io
import os.path

import git

from ogre.repository import Repository, Item


def test_repo_returns_items_when_iterated(repository):
    repo = Repository(repository)
    item = list(repo)[0]
    assert item.gbl_json.endswith('/foo/bar/geoblacklight.json')


def test_item_has_file_properties():
    item = Item('tests/fixtures/repo/foo/bar')
    assert item.fgdc == 'tests/fixtures/repo/foo/bar/fgdc.xml'


def test_update_pulls_changes_from_remote(repository, remote):
    repo = Repository(repository)
    r = git.Repo(remote)
    r.index.commit('A new commit')
    repo.update()
    assert repo.repo.commit().message == 'A new commit'
