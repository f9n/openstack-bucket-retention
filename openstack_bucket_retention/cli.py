import logging

import click

from . import __version__
from .core import retention

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.group()
@click.pass_context
def main(ctx):
    ctx.ensure_object(dict)


@main.command("version")
def version_cmd():
    """
    Show version
    """
    click.echo(f"openstack-bucket-retention: {__version__}")


@main.command("run")
@click.option("--bucket-name", required=True, help="Bucket (Container) Name")
@click.option(
    "--retention-time",
    default="1w",
    help="Retention Time. Examples: 1s, 1m, 1h, 1d, 1w",
)
def run_cmd(bucket_name, retention_time):
    """
    Run retention
    """
    retention(bucket_name, retention_time)
