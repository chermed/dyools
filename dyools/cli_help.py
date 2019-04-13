from __future__ import (absolute_import, division, print_function, unicode_literals)

import os

import click
import polib

from .klass_path import Path
from .klass_print import Print
from .klass_yaml_config import YamlConfig

DATABASE_PATH = Path.create_dir(os.path.join(Path.home(), '.dyvz', 'po_databases'))


@click.group()
def cli_help():
    pass


@cli_help.command('list')
def __list():
    """
CLI: command line interfaces :
------------------------------
    - etl: realize a workflow of a real ETL (extract, transform, Load, process errors)
    - dhelp: show the manual of the api
    - job: execute a bunch of commands, possible to use them in a loop with some prompts
    - po: make a database of translations and help translating a file
    - sign: save time passed on a project by date and show it on a calendar
    - todo: save tasks to do
    - tool: contains random cli and fake command line interfaces
    - ws_agent: launch a python agent on a server, iby default launched on 0.0.0.0:5000 (use the class Consummer to
    intercat with it)
    - xml: receive an xml in the STDIN and parse them (a separator may be use) and offer the possiblity to extract xpaths

Decorators:
-----------
    - log: Log arguments, response and elpsed time when executing a function
    - raise_exception: for functions that return a boolean, it is possible with this decorator to raise an exception if

Misc:
-----
    - connector, job: generic connector and job utilities for the ETL, see 'etl' for more information
    - odooconnector, odoojob: odoo connector and job utilities for the ETL, see 'etl' for more information
    - csvconnector, csvjob: odoo connector and job utilities for the ETL, see 'etl' for more information
    - consumer: communicate with the remote python agent (ws_agent)


    """
    Print.info(__list.__doc__)

@cli_help.command('raise_exception')
def __raise_exception():
    """
raise_exception: for functions that return a boolean, it is possible with this decorator to raise an exception if the
function returns False

    from dyools import raise_exception
    @raise_exception(exception=TypeError, exception_msg='[%s] is not valid', arg_index=1)
    def foo(x..):
       pass

default arguments:
    1 - exception = Exception,
    2 - exception_msg = 'Error'
    3 - arg_index = -1

    """
    Print.info(__raise_exception.__doc__)

@cli_help.command('log')
def __log():
    """
log: this decorator logs :
    1 - arguments and theirs types
    2 - response and its type
    3 - elapsed time in seconds

    from dyools import log
    @log
    def foo(x..):
       pass
    """
    Print.info(__log.__doc__)


@cli_help.command('etl')
def __etl():
    """
ETL: Extract, Transform, Load and process errors

Configuration steps:
--------------------
1 - Create two connectors class for source an destination streams
A connector should inherit from Connector class and define the method 'get' that should open a stream

    from dyools import Connector
    class CLASS_A(Connector):
        def get(self):
            # self contains params token from configuration file
            # self.params['param_1'] => value_1
            return open_stream...


2 - Create an extractor class
An extractor class should inherit from JobExtractorAbstract class and define the methods 'load' and 'count'
    - self.context contains information about source/destination streams and global job information
    - self.params contains parameters about the related stream
    - self.X can return information about the split : self.offset, self.limit, self.domain


    class ProductExtractor(JobExtractorAbstract):
        def extract(self, methods, queued_data, pool):
            # methods: are the chain in the pipeline
            # queued_data: data to process
            # pool: list to fill before quit
            # if necessary self.get_source() return the source stream
            return pool.append((methods, new_data))

        def count(self):
            # if necessary self.get_source() and self.get_destination() returns the two streams
            return X

3 - Create a transformer class
A transformer class should inherit from JobTransformerAbstract class and define the methods 'transform'
    - self.context contains information about source/destination streams and global job information
    - self.params contains parameters about the related stream
    - self.X can return information about the split : self.offset, self.limit, self.domain


    class ProductTransform(JobTransformerAbstract):
        def transform(self, methods, queued_data, pool):
            # methods: are the chain in the pipeline
            # queued_data: data to process
            # pool: list to fill before quit
            # if necessary self.get_source() return the source stream
            return pool.append((methods, new_data))

4 - Create a loader class
A loader class should inherit from JobLoaderAbstract class and define the methods 'load'
    - self.context contains information about source/destination streams and global job information
    - self.params contains parameters about the related stream
    - self.X can return information about the split : self.offset, self.limit, self.domain


    class ProductLoader(JobLoaderAbstract):
        def load(self, methods, queued_data, pool):
            # methods: are the chain in the pipeline
            # queued_data: data to process
            # pool: list to fill before quit
            # if necessary self.get_source() return the source stream
            return pool.append((methods, new_data))

5 - Create an error processing class
An error processing class should inherit from JobErrorAbstract class and define the methods 'transform'
    - self.context contains information about source/destination streams and global job information
    - self.params contains parameters about the related stream
    - self.X can return information about the split : self.offset, self.limit, self.domain


    class ProductError(JobErrorAbstract):
        def error(self, methods, queued_data, pool):
            # methods: are the chain in the pipeline
            # queued_data: data to process
            # pool: list to fill before quit
            # if necessary self.get_source() return the source stream
            return pool.append((methods, new_data))


6 - Create a migrate file configuration
Example of a configuration file
        connectors:
          source_a: con.py::CLASS_A
          source_b: con.py::CLASS_B
        params:
          source_a:
            param_1: value_1
            param_2: value_2
          source_b:
            param_1: value_1
            param_2: value_2
        jobs:
          - extract: product_template.py::Template
            load: product_template.py::Template
            transform: product_template.py::Template
            error: product_template.py::Template
            priority: 1
            threads: 6
            limit: 50
            active: 1
            tag: product_template

7 - Launch the pipeline
Commands :
    etl -c PATH_TO_MIGRATE_FILE --logfile=PATH_TO_OPTIONNAL_LOG_FILE
    etl -c --start=PRIORITY_START --stop=PRIORITY_STOP
    etl -c --select=PRIORITY_1,PRIORITY_2,PRIORITY_3
    etl -c --tags=TAG_A,TAG_B

Odoo Implementation:
--------------------
1 - Create two connectors classes for source an destination streams

    class SOURCE_DB(OdooConnector):
        pass

    class SOURCE_DESTINATION(OdooConnector):
        pass

2 - Create job classes for each object to migrate

    from dyools import OdooJobExtractor, OdooJobLoader, OdooJobTransformer, OdooJobError

    class Partner(OdooJobExtractor, OdooJobTransformator, OdooJobLoader, OdooJobError):
        _source_name = 'res.partner'
        _destination_name = 'res.partner'
        _source_fields = ['id', 'name', ]
        _destination_fields = ['id', 'name',  ]
        _destination = 's_db'
        _source = 'd_db'

        def transform(self, methods, queued_data, pool):
            # transform data
            pool.append((methods, queued_data))
3 - Create a migrate file configuration
Example of a configuration file

    connectors:
      s_db: con.py::SOURCE_DB
      d_db: con.py::SOURCE_DESTINATION
    params:
      s_db:
        host: localhost
        port: 8069
        user: admin
        password: admin
        dbname: SOURCE
      d_db:
        host: localhost
        port: 8069
        user: admin
        password: admin
        dbname: DESTINATION
    jobs:
      - extract: res_partner.py::Partner
        load: res_partner.py::Partner
        transform: res_partner.py::Partner
        error: res_partner.py::Partner
        priority: 1
        threads: 6
        limit: 50
        active: 1
        tag: partners

    Automatically OdooLoader use Load to send datas, if a create/write is required with a test by keys, in the job, add :
        primary_keys:
          - name
          - city

CSV Implementation:
-------------------
1 - Create a connector class for the CSV source stream

    class SOURCE_CSV(CsvConnector):
        pass

2 - Create job extractor class

    from dyools import CsvJobExtractor

    class Partner(CsvJobExtractor):
        pass

3 - Create a migrate file configuration
Example of a configuration file

    connectors:
      s_csv: con.py::SOURCE_CSV
      ...
    params:
      s_csv:
        path: PATH_TO_CSV.CSV
      ...
    jobs:
      - extract: res_partner.py::Partner
        ...
    """
    Print.info(__etl.__doc__)

