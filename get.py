"""
This module create the configuration

Copyright (c) 2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""

import kddi.data as d


def init_connection(host, port, login, password):
    connection = d.connect(host, port, login, password)
    return connection


def get_configuration(connection, session, filter):
    try:
        print(d.get_config(connection, filter, session))

    except Exception as e:
        print(e)


def close_connection(connection):
    connection.close_session()


if __name__ == '__main__':
    host = '10.1.7.84'
    host2 = '10.1.7.66'
    port = 830
    login = 'root'
    password = 'netlabN.'

    # configuration files
    config_transceiver_file = 'transceiver_config.xml'
    config_topology_file = 'node_topology_config.xml'
    config_connection_file = 'node_connectivity_config.xml'

    # filters
    filter_transceiver = "<transceiver/>"
    filter_topology = "<node/>"
    filter_connection = "<connection/>"

    connectionRX = init_connection(host, port, login, password)
    get_configuration(connectionRX, 'running', filter_connection)
    close_connection(connectionRX)

    connectionRX = init_connection(host2, port, login, password)
    get_configuration(connectionRX, 'running', filter_connection)
    close_connection(connectionRX)
