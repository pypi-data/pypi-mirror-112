#!/usr/bin/env python

# Copyright 2021 Element Analytics, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys

sys.dont_write_bytecode = True
PYTHONDONTWRITEBYTECODE = 1
import click
from unify.properties import Properties
from unify.apimanager import ApiManager
from unify.apiutils import tabulate_from_json
from tabulate import tabulate
import json


def print_stdr(value):
    if value is None:
        return

    text = repr(value)

    try:
        sys.stdout.write(value)
    except UnicodeEncodeError:
        bytes = text.encode(sys.stdout.encoding, 'backslashreplace')
        if hasattr(sys.stdout, 'buffer'):
            sys.stdout.buffer.write(bytes)
        else:
            text = bytes.decode(sys.stdout.encoding, 'strict')
            sys.stdout.write(text)
    sys.stdout.write("\n")


def get_piped_param(ctx, param, value):
    if not value and not click.get_text_stream('stdin').isatty():
        return click.get_text_stream('stdin').read().strip()
    else:
        return value


@click.group()
def cli():
    pass


@cli.group()
def cluster():
    """Configuration Setup for Element Unify"""
    pass


@cluster.command('add')
@click.option('--remote', prompt=True, hide_input=False, required=True, confirmation_prompt=False, type=click.STRING)
@click.option('--username', prompt=True, hide_input=False, required=True, confirmation_prompt=False, type=click.STRING)
@click.option('--password', prompt=True, hide_input=True, required=True, confirmation_prompt=False, type=click.STRING)
@click.option('--name', prompt=True, hide_input=False, required=False, default=None, confirmation_prompt=False,
              type=click.STRING)
@click.option('--assetsync', hide_input=False, default=False, type=click.BOOL)
def add_cluster(remote, username, password, name, assetsync):
    """Create a new remote cluster"""
    try:
        Properties().store_cluster(username=username, password=password, cluster=remote, name=name, assetsync=assetsync)
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@cluster.command('login')
@click.option('--remote', prompt=False, hide_input=False, required=False, confirmation_prompt=False, type=click.STRING)
def login(remote):
    """Login to a given Element Unify Cluster"""

    try:
        auth = ApiManager(cluster=remote).orgs.auth_token()
        Properties().set_auth_token(token=auth, cluster=remote)
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@cluster.command('default')
@click.option('--remote', prompt=True, hide_input=False, required=True, confirmation_prompt=False, type=click.STRING)
def set_default(remote):
    """Login to a given Element Unify Cluster"""
    try:
        Properties().set_default(name=remote)
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@cluster.command('list')
def list_cluster():
    """List all available clusters"""
    try:
        clusters = Properties().get_all_clusters()
        click.echo(click.style(tabulate(tabulate_from_json(clusters), "keys"), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@cluster.command('disconnect')
@click.option('--remote', prompt=True, hide_input=False, confirmation_prompt=False, type=click.STRING)
def disconnect_cluster(remote):
    """List all available clusters"""
    click.confirm('Do you want to disconnect from {}?'.format(remote), abort=True)
    try:
        Properties().remove_cluster(name=remote)
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@cli.group()
def user():
    """Group for the user related commands"""
    pass


@cli.group()
def template():
    """Group for template commands"""
    pass


@template.command('show')
@click.option('--remote', prompt=True, hide_input=False, confirmation_prompt=False, type=click.STRING)
@click.option('--org', prompt="Org id", hide_input=False, default=None, required=True, type=click.INT)
def show_templates(remote, org):
    try:
        response = ApiManager(cluster=remote).templates.list_asset_templates(org_id=org)
        click.echo(click.style(tabulate(tabulate_from_json(response), "keys"), blink=False, bold=True, fg='green'))

    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@cli.group()
def pipeline():
    """Group for pipeline commands"""
    pass


@pipeline.command('list')
@click.option('--org', prompt="Org id", hide_input=False, default=None, required=True, type=click.INT)
@click.option('--remote', prompt=False, hide_input=False, required=False, confirmation_prompt=False, type=click.STRING)
@click.option('--table', '-t', is_flag=True, help="Print in table")
def list_pipeline(org, remote, table):
    try:
        response = ApiManager(cluster=remote).pipeline_list(org_id=org)
        if table:
            response = tabulate_from_json(response)
            click.echo(click.style(tabulate(response, "keys"), blink=False, bold=True, fg='green'))
        else:
            click.echo(click.style(json.dumps(response), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@cli.group()
def wf():
    """
    Group for work flow commands
    :return:
    """
    pass


@wf.command('export-template')
@click.option('--remote', prompt=True, hide_input=False, confirmation_prompt=False, type=click.STRING)
@click.option('--org', prompt="Org id", hide_input=False, default=None, required=True, type=click.INT)
def export_template(remote, org):
    try:
        response = ApiManager(cluster=remote).templates.download_all_templates(org_id=org)
        click.echo(response)
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@wf.command('import-template-config')
@click.option('--remote', prompt=True, hide_input=False, confirmation_prompt=False, type=click.STRING)
@click.option('--org', prompt="Org id", hide_input=False, default=None, required=True, type=click.INT)
@click.argument('content', callback=get_piped_param, required=False)
def import_template_config(remote, org, content):
    try:
        ApiManager(cluster=remote).templates.upload_config_with_content(org_id=org, content=content)
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@wf.command('export-template-config')
@click.option('--remote', prompt=True, hide_input=False, confirmation_prompt=False, type=click.STRING)
@click.option('--org', prompt="Org id", hide_input=False, default=None, required=True, type=click.INT)
def export_template_config(remote, org):
    try:
        response = ApiManager(cluster=remote).templates.download_all_template_config(org_id=org)
        click.echo(response)
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@wf.command('import-template')
@click.option('--remote', prompt=True, hide_input=False, confirmation_prompt=False, type=click.STRING)
@click.option('--org', prompt="Org id", hide_input=False, default=None, required=True, type=click.INT)
@click.argument('content', callback=get_piped_param, required=False)
def import_template(remote, org, content):
    try:
        ApiManager(cluster=remote).templates.upload_string_content_file(org_id=org, content=content)
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@wf.command('export-pipeline')
@click.option('--remote', prompt=True, hide_input=False, confirmation_prompt=False, type=click.STRING)
@click.option('--org', prompt="Org id", hide_input=False, default=None, required=True, type=click.INT)
@click.option('--pipeline', prompt="Pipeline id", hide_input=False, default=None, required=True, type=click.INT)
@click.option('--skip', multiple=True, required=False, default=[])
def export_pipeline(remote, org, pipeline, skip):
    try:
        response = ApiManager(cluster=remote).create_pipeline_export_data(
            org_id=org,
            pipeline_id=pipeline,
            skip=skip
        )
        click.echo(response)
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@wf.command('import-pipeline')
@click.option('--remote', prompt=True, hide_input=False, confirmation_prompt=False, type=click.STRING)
@click.option('--org', prompt="Org id", hide_input=False, default=None, required=True, type=click.INT)
@click.option('--deduplicate', prompt=False, hide_input=False, default='clone', required=False,
              type=click.Choice(['clone', 'error']))
@click.option('--skip', multiple=True, required=False, default=[])
@click.argument('content', callback=get_piped_param, required=False)
def import_pipeline(remote, org, deduplicate, content, skip):
    try:
        response = ApiManager(cluster=remote).proceses_importing_pipeline_file(
            org_id=org,
            content=content,
            handleduplicates=deduplicate,
            skip=skip
        )

        click.echo(click.style(str(response), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@wf.command('export-dataset')
@click.option('--org', prompt="Org id", hide_input=False, default=None, required=True, type=click.INT)
@click.option('--remote', prompt=False, hide_input=False, required=False, confirmation_prompt=False, type=click.STRING)
@click.option('--id', multiple=True, required=False, default=[])
def export_dataset(org, remote, id):
    try:
        response = ApiManager(cluster=remote).export_source(
            org_id=org,
            dataset_ids=id
        )
        click.echo(click.style(str(response), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@wf.command('import-dataset')
@click.option('--org', prompt="Org id", hide_input=False, default=None, required=True, type=click.INT)
@click.option('--remote', prompt=False, hide_input=False, required=False, confirmation_prompt=False, type=click.STRING)
@click.argument('content', callback=get_piped_param, required=False)
def import_dataset(org, remote, content):
    try:

        response = ApiManager(cluster=remote).import_sources(
            org_id=org,
            pipeline_id=None,
            content=content,
            update_pipeline=False
        )
        click.echo(click.style(str(response), blink=False, bold=True, fg='green'))

    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@wf.command('export-dataset')
@click.option('--org', prompt="Org id", hide_input=False, default=None, required=True, type=click.INT)
@click.option('--remote', prompt=False, hide_input=False, required=False, confirmation_prompt=False, type=click.STRING)
@click.option('--id', multiple=True, required=False, default=[])
def export_dataset(org, remote, id):
    try:
        response = ApiManager(cluster=remote).export_source(
            org_id=org,
            dataset_ids=id
        )
        click.echo(click.style(str(response), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@wf.command('import-dataset')
@click.option('--org', prompt="Org id", hide_input=False, default=None, required=True, type=click.INT)
@click.option('--remote', prompt=False, hide_input=False, required=False, confirmation_prompt=False, type=click.STRING)
@click.argument('content', callback=get_piped_param, required=False)
def import_dataset(org, remote, content):
    try:

        response = ApiManager(cluster=remote).import_sources(
            org_id=org,
            pipeline_id=None,
            content=content,
            update_pipeline=False
        )
        click.echo(click.style(str(response), blink=False, bold=True, fg='green'))

    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@wf.command('export-function')
@click.option('--remote', prompt=True, hide_input=False, confirmation_prompt=False, type=click.STRING)
@click.option('--org', prompt="Org id", hide_input=False, default=None, required=True, type=click.INT)
@click.option('--function', prompt="Function id", hide_input=False, default=None, required=True, type=click.STRING)
@click.option('--skip', multiple=True, required=False, default=[])
def export_function(remote, org, function, skip):
    try:
        response = ApiManager(cluster=remote).create_pipeline_export_data(
            org_id=org,
            pipeline_id=function,
            skip=skip
        )
        click.echo(response)
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@wf.command('import-function')
@click.option('--remote', prompt=True, hide_input=False, confirmation_prompt=False, type=click.STRING)
@click.option('--org', prompt="Org id", hide_input=False, default=None, required=True, type=click.INT)
@click.option('--deduplicate', prompt=False, hide_input=False, default='clone', required=False,
              type=click.Choice(['clone', 'error']))
@click.option('--skip', multiple=True, required=False, default=[])
@click.argument('content', callback=get_piped_param, required=False)
def import_function(remote, org, deduplicate, content, skip):
    try:
        response = ApiManager(cluster=remote).proceses_importing_pipeline_file(
            org_id=org,
            content=content,
            handleduplicates=deduplicate,
            skip=skip,
            function=True
        )

        click.echo(click.style(str(response), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@cli.group()
def dataset():
    """Group for dataset commands"""


@dataset.command('add')
@click.option('--orgid', prompt="Org id", hide_input=False, default=None, required=True, type=click.INT)
@click.option('--remote', prompt=False, hide_input=False, required=False, confirmation_prompt=False, type=click.STRING)
@click.option('--dtype', prompt="Dataset Type", hide_input=False, default='external', required=False,
              type=click.Choice(['external', 'piconfig']))
@click.option('--name', prompt="Dataset Name", hide_input=False, default=None, required=True, type=click.STRING)
@click.argument('content', callback=get_piped_param, required=False)
def add_dataset(orgid, remote, dtype, name, content):
    try:
        response = ApiManager(cluster=remote).import_source(content=content, orgid=orgid, name=name, type=dtype)
        click.echo(click.style(str(response), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@dataset.command('big')
@click.option('--orgid', prompt="Org id", hide_input=False, default=None, required=True, type=click.INT)
@click.option('--remote', prompt=False, hide_input=False, required=False, confirmation_prompt=False, type=click.STRING)
@click.option('--name', prompt="Dataset Name", hide_input=False, default=None, required=True, type=click.STRING)
@click.option('--encoding', prompt="file encoding", hide_input=False, default='UTF-8', required=True, type=click.STRING)
@click.option('--chunks', prompt="Number of rows", hide_input=False, default=10000, required=True, type=click.INT)
@click.argument('content', callback=get_piped_param, required=False)
def add_big_dataset(orgid, remote, name, encoding, chunks, content):
    try:
        response = ApiManager(cluster=remote).import_source(
            content=content,
            orgid=orgid,
            name=name,
            type="generic",
            chunks=chunks,
            encoding=encoding
        )
        print(response)
        click.echo(click.style(str(response), blink=False, bold=True, fg='green'))

    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@dataset.command('append')
@click.option('--orgid', prompt="Org id", hide_input=False, default=None, required=True, type=click.INT)
@click.option('--remote', prompt=False, hide_input=False, required=False, confirmation_prompt=False, type=click.STRING)
@click.option('--datasetid', prompt=False, hide_input=False, required=False, confirmation_prompt=False,
              type=click.STRING)
@click.argument('content', callback=get_piped_param, required=False)
def append_dataset(orgid, remote, datasetid, content):
    try:
        response = ApiManager(cluster=remote).append_data(content=content, orgid=orgid, dataset_id=datasetid)
        click.echo(click.style(str(response), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@dataset.command('list')
@click.option('--org', prompt="Org id", hide_input=False, default=None, required=True, type=click.INT)
@click.option('--remote', prompt=False, hide_input=False, required=False, confirmation_prompt=False, type=click.STRING)
@click.option('--table', '-t', is_flag=True, help="Print in table")
def list_dataset(org, remote, table):
    try:
        response = ApiManager(cluster=remote).dataset_list(org_id=org)
        if table:
            response = tabulate_from_json(response)
            click.echo(click.style(tabulate(response, "keys"), blink=False, bold=True, fg='green'))
        else:
            click.echo(click.style(json.dumps(response), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@user.command('list')
def user_list():
    click.echo(click.style("Command under development", blink=False, bold=True, fg='blue'))


@user.command('add')
@click.option('--orgid', prompt="Org id", hide_input=False, default=None, required=True, type=click.INT)
@click.option('--email', prompt="User Email", hide_input=False, default=None, required=True, type=click.STRING)
@click.option('--name', prompt="Person Name", hide_input=False, default=None, required=True, type=click.STRING)
@click.option('--role', prompt="User Role", hide_input=False, default='Contributor', required=False,
              type=click.Choice(['Admin', 'Contributor']))
@click.option('--remote', prompt=False, hide_input=False, required=False, confirmation_prompt=False, type=click.STRING)
def user_add(orgid, email, name, role, remote):
    try:
        response = ApiManager(cluster=remote).orgs.invite_user(org_id=orgid, email=email, name=name, role=role)
        click.echo(click.style(str(response), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@cli.group()
def org():
    """Group for org related commands"""
    pass


@org.command('list')
@click.option('--table', prompt=False, default=True, required=False, type=click.BOOL)
@click.option('--remote', prompt=False, hide_input=False, required=False, confirmation_prompt=False, type=click.STRING)
def org_list(table, remote):
    try:
        response = ApiManager(cluster=remote).orgs.get_org_list()

        if table:
            response = tabulate_from_json(response)

        click.echo(click.style(tabulate(response, "keys"), blink=False, bold=True, fg='green'))

    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@org.command('add')
@click.option('--name', prompt="Org Name", hide_input=False, confirmation_prompt=False, type=click.STRING)
@click.option('--remote', prompt=False, hide_input=False, required=False, confirmation_prompt=False, type=click.STRING)
def org_add(name, remote):
    try:
        response = ApiManager(cluster=remote).orgs.create_organization(org_name=name)
        click.echo(click.style(str(response), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@org.command('delete')
@click.option('--orgid', prompt="Org id", hide_input=False, default=None, required=False, type=click.INT)
@click.option('--remote', prompt=False, hide_input=False, required=False, confirmation_prompt=False, type=click.STRING)
def org_delete(orgid, remote):
    click.confirm('Do you want to delete org {}? this cant be undone '.format(orgid), abort=True)
    try:
        response = ApiManager(cluster=remote).orgs.delete_organization(org_id=orgid)
        click.echo(click.style(str(response), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@cli.group()
def access():
    """Group for Element Unify Access related commands"""
    pass


@access.command('execute')
@click.option('--remote', prompt=False, hide_input=False, required=False, confirmation_prompt=False, type=click.STRING)
@click.option('--orgid', prompt="Org id", hide_input=False, default=None, required=False, type=click.INT)
@click.option('--format', prompt=False, hide_input=False, default='csv', required=False,
              type=click.Choice(['table', 'csv', 'json']))
@click.argument('query', callback=get_piped_param, required=True)
def execute_query(remote, orgid, format, query):
    try:
        response = ApiManager(cluster=remote).execute_query(query=query, orgid=orgid, format=format)

        if format == "table":
            response = tabulate_from_json(response)
            click.echo(click.style(tabulate(response, "keys"), blink=False, bold=True, fg='green'))
        else:
            click.echo(click.style(str(response), blink=False, bold=True, fg='green'))

    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


@access.command('databases')
@click.option('--remote', prompt=False, hide_input=False, required=False, confirmation_prompt=False, type=click.STRING)
@click.option('--orgid', prompt="Org id", hide_input=False, default=None, required=False, type=click.INT)
def get_databases(remote, orgid):
    try:
        response = ApiManager(cluster=remote).assethub_access_tables(orgid=orgid)
        response = tabulate_from_json(response)
        click.echo(click.style(tabulate(response, "keys"), blink=False, bold=True, fg='green'))
    except Exception as err:
        click.echo(click.style(str(err), blink=False, bold=True, fg='red'))


if __name__ == '__main__':
    cli()
