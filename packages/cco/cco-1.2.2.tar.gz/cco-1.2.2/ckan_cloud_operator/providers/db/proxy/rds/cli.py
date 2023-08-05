import click
import datetime
import traceback

from ckan_cloud_operator import logs

from . import manager


@click.group()
def rds():
    """Manage the RDS centralized db proxy"""
    pass


@rds.command()
def port_forward():
    while True:
        start_time = datetime.datetime.now()
        try:
            manager.start_port_forward()
        except Exception:
            traceback.print_exc()
        end_time = datetime.datetime.now()
        if (end_time - start_time).total_seconds() < 10:
            logs.critical('DB Proxy failure')
            logs.exit_catastrophic_failure()
        else:
            logs.warning('Restarting the DB proxy')


@rds.command()
def initialize():
    manager.initialize()
    logs.exit_great_success()
