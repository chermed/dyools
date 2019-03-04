from __future__ import (absolute_import, division, print_function, unicode_literals)

import logging

import click

from .klass_ws import WS

logger = logging.getLogger(__name__)


@click.command()
@click.option('--logfile', '-l',
              type=click.Path(file_okay=True, dir_okay=False, writable=True, readable=True, resolve_path=True,
                              allow_dash=True), required=False, )
@click.option('--host', '-h', type=click.STRING, default='0.0.0.0')
@click.option('--port', '-p', type=click.INT, default=5000)
@click.option('--token', '-t', type=click.STRING, default=None)
@click.option('--name', '-n', type=click.STRING, default=None)
@click.pass_context
def start_agent(ctx, logfile, host, port, token, name):
    """Command line for agent"""
    ws_kwargs = {}
    if host: ws_kwargs['host'] = host
    if port: ws_kwargs['port'] = port
    if token: ws_kwargs['token'] = token
    if name: ws_kwargs['name'] = name
    ws = WS(**ws_kwargs)
    if logfile:
        logging.basicConfig(filename=logfile, level=logging.DEBUG)
    ws.start()