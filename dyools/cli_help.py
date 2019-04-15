from __future__ import (absolute_import, division, print_function, unicode_literals)

import os

import click

from .klass_path import Path
from .klass_print import Print

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
    - convert: convert data type and time (MB -> GB, seconds -> hours)
    - counter: a helper to compute the elapsed time
    - data: a data wrapper and normalizer, the aim of this class to compute header (list) and lines (list pf lists)
    - date: work with string dates
    - df: a simple dataframe object with operations 'add' and 'remove', each data is a Serie object
    - serie: a simple Serie object
    - eval: evaluate variables within a data structure
    - inspect: inspect source code
    - is: check a type


    """
    Print.info(__list.__doc__)


@cli_help.command('raise_exception')
def __raise_exception():
    """raise_exception: for functions that return a boolean, it is possible with this decorator to raise an exception if the
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
    """log: this decorator logs :
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
    """ETL: Extract, Transform, Load and process errors

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


@cli_help.command('consumer')
def __consumer():
    """Consumer: communicate with remote python agent, for the security reason, use a token

    from dyools import Consumer
    c = Consumer(host='127.0.0.1', port=5000, token=None)
    c.ping()  #check if remote agent is up
    c.info()  #see variables available on the agent
    c.flush() #remove all results in the local
    c.print() #print the result
    c.stop()  #shutdown the remote agent

1 - Execute OS commands :

    from dyools import Consumer
    c = Consumer(host='127.0.0.1', port=5000)
    c.add(['ls','-alh'])
    c.add(['ls'])
    c.cmdline()
    c.print()

    OR :

    from dyools import Consumer
    c = Consumer(host='127.0.0.1', port=5000)
    c.cmdline(['ls','-alh'])
    c.print()

2 - Execute python expressions :

    from dyools import Consumer
    c = Consumer(host='127.0.0.1', port=5000)
    c.add('import os;import sys')
    c.add('dirs = os.listdir();a = 8;b = 10')
    c.add('tbl = {"a": 20, "b": 40}')
    c.console()
    c.print_dirs() #pprint a variable
    c.data_dirs()  #return the value of a variable
    c.table_tbl()
    c.print_b()

    OR :

    from dyools import Consumer
    c = Consumer(host='127.0.0.1', port=5000)
    c.console('b = 33')
    c.print_b()


3 - Get OS stats: disk usage, cpu and memory usage

    from dyools import Consumer
    c = Consumer(host='127.0.0.1', port=5000)
    c.top()    #get a summary of a top command
    c.top(['/tmp', '/bin', '/usr']) #get a summary of a top command with the disk usage of some paths

    """
    Print.info(__consumer.__doc__)


@cli_help.command('convert')
def __convert():
    """Convert: convert data types and time types, units are not case sensible

1 - Convert data types

    from dyools import Convert
    mb = 1024 #variable in megabytes (units: ["B", "K", "M", "G", "T", "P", "E", "Z", "Y"])
    Convert.data(mb, 'mb', 'gb') #=> 1.0 (float)
    Convert.data(mb, 'mb', 'gb', r=2) #=> 1.0 (float) with a round

1 - Convert time types

    from dyools import Convert
    seconds = 3600 #variable in seconds (units: ["MS", "S", "M", "H"])
    Convert.time(seconds, 's', 'm') #=> 60.0 (float)
    Convert.time(seconds, 's', 'h') #=> 1.0 (float)
    Convert.time(seconds, 's', 'h', r=2) #=> 1.0 (float) using a round
    """
    Print.info(__convert.__doc__)


@cli_help.command('counter')
def __counter():
    """Counter: compute the time elapsed after an execution

    from dyools import Counter
    c = Counter('A test counter') #the name is optional, automatically the counter is started
    c.start()    #start the counter
    c.restart()  #restart the counter
    c.stop()     #stop the counter
    c.resume()   #resume the counter
    c._get_elapsed_time()   #get a dictionnary of data: hours, minutes, seconds and total
    c.to_str(r=True, title='')   #get the string, by default the round is active and title is empty
    c.print(r=True, title='')    #print the string to the console
    """
    Print.info(__counter.__doc__)


@cli_help.command('data')
def __data():
    """Data: a data wrapper

    from dyools import Data
    d = Data(data, has_header=True, header=[], name='__NAME')

Data can be :
    - dictionary of dictionaries (not need for header, the wrapper will compute them, the parent key will mapped with the
    value of name='__NAME')
    - dictionary of values (not need for header, the wrapper will compute them)
    - list of dictionaries (not need for header, the wrapper will compute them)
    - list of lists (has_header=True to specify if the first item is a header else  give a header)
    - list of values (has_header=True to specify if the data is a header else give a header)
    - object (should specify the header to get attributes)


    from dyools import Data
    d = Data(data, has_header=True, header=[], name='__NAME')
    d.get_header()         #return header
    d.get_default_header() #return header if computed else if there are some lines, an index will be generated
    d.get_lines()          #return data lines
    d.get_pretty_table(pretty=True, add_index=False, grep=False, index=False) #return the Prettytable object
    d.get_html()           #get the html
    d.to_list()            #get a list of two list, the first item is the header, the second is the list of lines
    d.to_dictlist()        #get a list of dictionaries
    d.show(pretty=True, add_index=False, grep=False, index=False, header=False, footer=False, exit=False) #print to console
    """
    Print.info(__data.__doc__)


@cli_help.command('date')
def __date():
    """Data: work with string dates
Date accepts string, date and datetime objects as argument and compute the default format
A format can be forced
If not argument is given the value will be the result of datetime.now()

Some global format are :
    - Date.DATETIME_FORMAT      '%Y-%m-%d %H:%M:%S'
    - Date.DATETIME_FR_FORMAT   '%d/%m/%Y %H:%M:%S'
    - Date.DATETIME_HASH_FORMAT '%Y%m%d_%H%M%S'
    - Date.DATE_FORMAT          '%Y-%m-%d'
    - Date.DATE_FR_FORMAT       '%d/%m/%Y'
    - Date.DATE_HASH_FORMAT     '%Y%m%d'

1 - Initialize the object


    from dyools import Date
    d = Date().to_str() #return a string of now format: YYYY-mm-dd HH:MM:SS
    d = Date().to_str(fmt='%Y') #return a string of now format: YYYY
    d = Date(fmt='%Y').to_str() #return a string of now format: YYYY
    d = Date(fmt='%Y').to_str() #return a string of now format: YYYY
    d = Date('2019-01-01').to_str() #return '2019-01-01'
    d = Date(date()).to_str() #return '2019-01-01'
    d = Date(date.today()).to_str() #return a string of today, format: YYYY-mm-dd
    d = Date(datetime.now()).to_str() #return a string of now, format: YYYY-mm-dd HH:MM:SS

2 - Transformation

    from dyools import Date
    d = Date()
    d.relativedelta(days=7, months=-2, years=1, hours=3, minutes=20, seconds=-30) #return a string after transformation
    d.apply(days=7, months=-2, years=1, hours=3, minutes=20, seconds=-30)         #return an object of Str
    d.set_format('%d') #change the default format
    d.last_day()    #return a string of last day format: default format
    d.fist_day()    #return a string of first day format: default format
    d.to_datetime() #return a datetime object
    d.to_date()     #return a date object
    d.to_fr()       #return a string with format Date.DATE_FR_FORMAT if date else Date.DATETIME_FR_FORMAT for datetime
    d.is_between('2019-01-01', date(2030, 3, 1))   #return a boolean if the date is between two date, the arguments will
    convert to Date before comparison

3 - Date range

    for dt in Date.date_range('2010-01-01', date(2030, 1, 23), months=3):
        print(dt)

3 - Operations
    1 - add values to Date: Date('2010-01-01') + '3m'  #=> '2010-04-01' list: ['d','m','y','H','M', 'S']
    2 - compare two objects or with strings Date('2019') > Date('2020') or Date('2019') > '2010-04-01'

    """
    Print.info(__date.__doc__)


@cli_help.command('df')
def __df():
    """DF: a simple dataframe object

    from dyools import DF
    d = DF(index=[0, 1], is_responsible=[True, False])
    d.add('name', ['Jean', 'Luc'])
    d.add('age', [30, 45])
    d.remove('index')
    """
    Print.info(__df.__doc__)


@cli_help.command('serie')
def __serie():
    """Serie: a simple Serie object
Operations:
    - addition
    - subtraction
    - division
    - multiplication

    from dyools import Serie
    s1 = Serie([1, 2, 3])
    s2 = Serie([10, 20, 30])
    s3 = Serie([100, 200, 300])
    s1+s2+s3 #return a Serie object that make a sum of each tuple => <Serie [111, 222, 333]>
    s1[0] #return the first item as a value
    s1[1:-1] #return the first item as a value
    """
    Print.info(__serie.__doc__)


@cli_help.command('eval')
def __eval():
    """Eval: evaluate variable in a data structure

    from dyools import Eval
    ctx = {'a': 3}
    data = {'m': [{'{a}': '{a}'}], 'n' : ['{a}', 6]}
    Eval(data, ctx).eval()                   #return {'m': [{3: 3}], 'n': [3, 6]}
    Eval(data, ctx).eval(eval_result=False)  #return {'m': [{'3': '3'}], 'n': ['3', 6]}
    Eval(data, ctx).eval(keep_classes=False) #by default classes founds after evaluation a kept in string
    """
    Print.info(__eval.__doc__)

@cli_help.command('inspect')
def __inspect():
    """Inspect: inspect source code

    from dyools import Inspect
    import os
    Inspect.signature(os.path.isfile)
    Inspect.source(os.path.isfile)
    """
    Print.info(__inspect.__doc__)
