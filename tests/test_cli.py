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
def rmock():
    with requests_mock.Mocker() as m:
        yield m


@pytest.fixture
def solr(rmock):
    rmock.post('mock://example.com/solr')
    return rmock


@pytest.fixture
def schema(rmock, json_schema):
    rmock.get('mock://example.com/schema', json=json_schema)
    return rmock


def test_index_adds_records_to_solr(runner, repository, solr):
    runner.invoke(main, ['index', 'mock://example.com/solr', repository,
                         '--no-validate'])
    req = solr.request_history[0]
    assert req.json() == {'add': {'doc': {'dc_identifier_s': 'foo-bar-baz'}}}


def test_index_commits_changes(runner, repository, solr):
    runner.invoke(main, ['index', 'mock://example.com/solr', repository,
                         '--no-validate'])
    req = solr.request_history[-1]
    assert req.json() == {'commit': {}}


def test_index_uses_auth(runner, repository, solr):
    runner.invoke(main, ['index', 'mock://example.com/solr', repository,
                         '--solr-user', 'foo', '--solr-password', 'bar',
                         '--no-validate'])
    req = solr.request_history[0]
    assert req.headers['Authorization'] == 'Basic Zm9vOmJhcg=='


def test_index_validates_records(runner, repository, solr, schema):
    res = runner.invoke(main, ['index', 'mock://example.com/solr',
                               repository, '--schema',
                               'mock://example.com/schema'])
    assert '\'dc_title_s\' is a required property' in res.output
