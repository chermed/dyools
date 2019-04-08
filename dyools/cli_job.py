from __future__ import (absolute_import, division, print_function, unicode_literals)

import codecs
import os
import subprocess
import time

import click

from .klass_convert import Convert
from .klass_data import Data
from .klass_path import Path
from .klass_print import Print
from .klass_str import Str
from .klass_yaml_config import YamlConfig

JOB_PATH = os.path.join(Path.home(), '.dyvz', 'jobs.yml')


@click.group()
@click.pass_context
def cli_job(ctx):
    yaml = YamlConfig(JOB_PATH, create_if_not_exists=True)
    ctx.obj = {}
    ctx.obj['yaml'] = yaml


@cli_job.command('create')
@click.argument('name', type=click.STRING, required=True)
@click.argument('data', type=click.STRING, required=True)
@click.option('--description', type=click.STRING, required=False)
@click.pass_context
def __create(ctx, name, data, description):
    """Create a job"""
    yaml = ctx.obj['yaml']
    if yaml.get(name=name):
        Print.error('the job [%s] already exists' % name)
    commands = [data]
    if os.path.isfile(data):
        commands = open(data).read().split('\n')
    yaml.add(name, description=description or '', commands=commands)
    yaml.dump()
    Print.success('The job [%s] is successfully added' % name)


@cli_job.command('update')
@click.argument('name', type=click.STRING, required=True)
@click.argument('data', type=click.STRING, required=True)
@click.option('--description', type=click.STRING, required=False)
@click.pass_context
def __update(ctx, name, data, description):
    """Update a job"""
    yaml = ctx.obj['yaml']
    if not yaml.get(name=name):
        Print.error('the job [%s] is not exists' % name)
    commands = [data]
    if os.path.isfile(data):
        commands = open(data).read().split('\n')
    yaml.add(name, description=description or name, commands=commands)
    yaml.dump()
    Print.success('The job [%s] is successfully updated' % name)


@cli_job.command('delete')
@click.argument('name', type=click.STRING, required=True)
@click.pass_context
def __delete(ctx, name):
    """Delete a job"""
    yaml = ctx.obj['yaml']
    if not yaml.get(name=name):
        Print.error('the job [%s] is not exists' % name)
    if click.confirm('Are you sure, you want to delete [%s] ?' % name):
        yaml.delete(name=name)
        yaml.dump()
        Print.success('The job [%s] is deleted' % name)
    else:
        Print.warning('Aborted')


@cli_job.command('list')
@click.argument('grep', type=click.STRING, required=False)
@click.pass_context
def __list(ctx, grep):
    """List all jobs"""
    yaml = ctx.obj['yaml']
    Data(yaml.get_list(), header=['name', 'description']).show(grep=grep)


def __execute_commands(commands):
    for command in commands:
        Print.info('Command : %s' % command)
        p = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        out, err = p.communicate()
        if err:
            Print.error(err)
        if out:
            Print.info(out)


@cli_job.command('run')
@click.argument('name', type=click.STRING, required=True)
@click.option('--number', '-n', type=click.INT, default=1, required=False)
@click.option('--sleep', '-e', type=click.INT, default=0, required=False)
@click.option('--prompt', is_flag=True, default=False)
@click.option('--clear', is_flag=True, default=False)
@click.option('--time', 'time_', is_flag=True, default=False)
@click.option('--inline', is_flag=True, default=False)
@click.pass_context
def __run(ctx, name, number, sleep, prompt, clear, time_, inline):
    """Run a job"""
    yaml = ctx.obj['yaml']
    commands = []
    description = name
    if os.path.isfile(name):
        with codecs.open(name, encoding='utf8', mode='r') as job_file:
            for line in job_file.readlines():
                line = line.strip()
                if not line:
                    continue
                if line.startswith('#') or line.startswith(';') or line.startswith('//'):
                    continue
                commands.append(line)
    elif inline:
        commands.append(name)
    else:
        data = yaml.get_values(name=name)
        if not data:
            Print.error('the job [%s] is not exists' % name)
        commands = data.get('commands', [])
        description = data.get('description', name)
    index = 0
    start = time.time()
    while number != 0:
        index += 1
        if clear:
            click.clear()
        Print.info('')
        elapsed_time = Str(Convert.time(time.time() - start, r=2), numeric=True, suffix='seconds')
        Print.info(('-' * 10) + 'times:%s time: %s' % (index, elapsed_time))
        Print.info(('-' * 10) + '%s' % description)
        __execute_commands(commands)
        number -= 1
        if number != 0:
            time.sleep(sleep)
            if prompt:
                if click.confirm('Continue ?'):
                    continue
                else:
                    break
