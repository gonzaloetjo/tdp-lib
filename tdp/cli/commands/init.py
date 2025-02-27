# Copyright 2022 TOSIT.IO
# SPDX-License-Identifier: Apache-2.0

import os
from pathlib import Path

import click

from tdp.cli.session import init_db
from tdp.cli.utils import collection_paths
from tdp.core.dag import Dag
from tdp.core.repository.repository import NoVersionYet
from tdp.core.service_manager import ServiceManager


@click.command(short_help="Init database / services in tdp vars")
@click.option(
    "--sqlite-path",
    envvar="TDP_SQLITE_PATH",
    required=True,
    type=Path,
    help="Path to SQLITE database file",
)
@click.option(
    "--collection-path",
    envvar="TDP_COLLECTION_PATH",
    required=True,
    callback=collection_paths,  # transforms list of path into list of Collection
    help=f"List of paths separated by your os' path separator ({os.pathsep})",
)
@click.option(
    "--vars", envvar="TDP_VARS", required=True, type=Path, help="Path to the tdp vars"
)
def init(sqlite_path, collection_path, vars):
    dag = Dag.from_collections(collection_path)
    init_db(sqlite_path)
    service_managers = ServiceManager.initialize_service_managers(dag, vars)
    for name, service_manager in service_managers.items():
        try:
            click.echo(f"{name}: {service_manager.version}")
        except NoVersionYet:
            click.echo(f"Initializing {name}")
            service_manager.initiliaze_variables(service_manager)
