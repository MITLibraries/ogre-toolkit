# -*- coding: utf-8 -*-
from __future__ import absolute_import

import click
from jsonschema import ValidationError
import requests

from ogre import Repository, create_validator


@click.group()
@click.version_option()
def main():
    pass


@main.command()
@click.argument('solr')
@click.argument('repository', nargs=-1)
@click.option('--solr-user')
@click.option('--solr-password')
@click.option('--schema',
              default='https://raw.githubusercontent.com/geoblacklight/'
                      'geoblacklight/v1.1.2/schema/geoblacklight-schema.json')
@click.option('--validate/--no-validate', default=True)
def index(solr, repository, solr_user, solr_password, schema, validate):
    if solr_user and not solr_password:
        solr_password = click.prompt('Solr password', hide_input=True)
    session = requests.Session()
    if solr_user and solr_password:
        session.auth = (solr_user, solr_password)
    if validate:
        req = requests.get(schema)
        check = create_validator(req.json()['properties']['layer'])
    for repo in repository:
        r = Repository(repo)
        for item in r:
            record = item.record
            if validate:
                try:
                    check(record)
                except ValidationError as e:
                    click.echo(e.message)
                    continue
            session.post(solr, json={"add": {"doc": record}})
    session.post(solr, json={"commit": {}})
