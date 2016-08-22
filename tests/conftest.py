# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os.path
import shutil
import tempfile

import git
import pytest


@pytest.yield_fixture(scope="session", autouse=True)
def temp_dir():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    tmp_dir = tempfile.mkdtemp(dir=current_dir)
    tempfile.tempdir = tmp_dir
    yield
    if os.path.isdir(tmp_dir):
        shutil.rmtree(tmp_dir)


@pytest.yield_fixture
def local():
    tmp = tempfile.mkdtemp()
    yield tmp
    shutil.rmtree(tmp)


@pytest.yield_fixture
def remote():
    tmp = tempfile.mkdtemp()
    repo_dir = os.path.join(tmp, 'repo')
    shutil.copytree(_fixture_path('repo'), repo_dir)
    r = git.Repo.init(repo_dir)
    r.index.add('*')
    r.index.commit('Init')
    yield repo_dir
    shutil.rmtree(tmp)


def _fixture_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        'fixtures', path)
