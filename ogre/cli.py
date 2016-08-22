# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os.path

import click
import requests

from ogre import Repository


@click.group()
@click.version_option()
def main():
    pass


@main.command()
@click.argument('solr')
@click.argument('repository', nargs=-1)
@click.option('--solr-user')
@click.option('--solr-password')
def index(solr, repository, solr_user, solr_password):
    if solr_user and not solr_password:
        solr_password = click.prompt('Solr password', hide_input=True)
    session = requests.Session()
    if solr_user and solr_password:
        session.auth = (solr_user, solr_password)
    for repo in repository:
        r = Repository(repo)
        for item in r:
            record = item.record
            session.post(solr, json={"add": {"doc": record}})
    session.post(solr, json={"commit": {}})
