#!/usr/bin/python

from speedtest import Speedtest
from speedtest import ConfigRetrievalError
from speedtest import HTTP_ERRORS
from speedtest import printer
from speedtest import SpeedtestCLIError
from speedtest import get_exception

try:
    from argparse import ArgumentParser as ArgParser
    from argparse import SUPPRESS as ARG_SUPPRESS
    PARSER_TYPE_INT = int
    PARSER_TYPE_STR = str
except ImportError:
    from optparse import OptionParser as ArgParser
    from optparse import SUPPRESS_HELP as ARG_SUPPRESS
    PARSER_TYPE_INT = 'int'
    PARSER_TYPE_STR = 'string'

import pymysql


def parse_args():
    description = ( 'This is a wrapper to speedtest.py to get results and store them into a MySQL Database')

    parser = ArgParser(description=description)
    # Give optparse.OptionParser an `add_argument` method for
    # compatibility with argparse.ArgumentParser
    try:
        parser.add_argument = parser.add_option
    except AttributeError:
        pass
    parser.add_argument('--user', default='root', type=PARSER_TYPE_STR,
                        help='Database user. Default "root"')
    parser.add_argument('--database', type=PARSER_TYPE_STR,
                        help='Database name.')

    options = parser.parse_args()
    if isinstance(options, tuple):
        args = options[0]
    else:
        args = options
    return args

def getSpeedtest():
    try:
        speedtest = Speedtest()
    except (ConfigRetrievalError, HTTP_ERRORS):
        printer('Cannot retrieve speedtest configuration')
        raise SpeedtestCLIError(get_exception())

    speedtest.get_best_server()
    speedtest.download()
    speedtest.upload()

    return speedtest

def saveResults(speedtest, user, database):
    results = speedtest.results
    cnx = pymysql.connect(user=user, database=database)
    cursor = cnx.cursor()
    add_server = ("INSERT IGNORE INTO connections_servers (id, name, host, lat, lon, latency) VALUES (%s, %s, %s, %s, %s, %s)");
    server_data = (results.server['id'], results.server['name'], results.server['host'], results.server['lat'], results.server['lon'], results.server['latency'])
    cursor.execute(add_server, server_data)

    add_measure = ("INSERT INTO connections_bandwidth (date, interface, bytes_received, bytes_sent, download, upload, ping, server_id, ip, lat, lon) VALUES (CURRENT_TIMESTAMP, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    measure_data = ("eth0", results.bytes_received, results.bytes_sent, results.download, results.upload, results.ping, results.server['id'], speedtest.config['client']['ip'], speedtest.config['client']['lat'], speedtest.config['client']['lon'])
    cursor.execute(add_measure, measure_data)

    # Make sure data is committed to the database
    cnx.commit()

    cursor.close()
    cnx.close()

if __name__ == '__main__':
    args = parse_args()

    speedtest = getSpeedtest()
    saveResults(speedtest, args.user, args.database)