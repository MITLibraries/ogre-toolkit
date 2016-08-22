# -*- coding: utf-8 -*-
from __future__ import absolute_import

from click.testing import CliRunner
import pytest
import requests_mock

from ogre.cli import main


@pytest.fixture
def runner():
    return CliRunner()


@pytest.yield_fixture
def solr():
    with requests_mock.Mocker() as m:
        m.post(requests_mock.ANY)
        yield m


def test_index_adds_records_to_solr(runner, repository, solr):
    runner.invoke(main, ['index', 'mock://example.com', repository])
    req = solr.request_history[0]
    assert req.json() == {'add': {'doc': {'dc_identifier_s': 'foo-bar-baz'}}}


def test_index_commits_changes(runner, repository, solr):
    runner.invoke(main, ['index', 'mock://example.com', repository])
    req = solr.request_history[-1]
    assert req.json() == {'commit': {}}


def test_index_uses_auth(runner, repository, solr):
    runner.invoke(main, ['index', 'mock://example.com', repository,
                         '--solr-user', 'foo', '--solr-password', 'bar'])
    req = solr.request_history[0]
    assert req.headers['Authorization'] == 'Basic Zm9vOmJhcg=='
