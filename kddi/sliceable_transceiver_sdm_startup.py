"""
This module create the configuration of one spectral super channel (slice)

Copyright (c) 2018-2019 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""

import data as d


def init_connection(host, port, login, password):
    connection = d.connect(host, port, login, password)
    return connection


def create_configuration(connection, config_file, session, operation, filter):
    try:
        f = open(config_file)
        d.edit_config(connection, f.read(), session, operation)
        f.close()
        print(d.get_config(connection, filter, session))

    except Exception as e:
        print(e)


def close_connection(connection):
    connection.close_session()


if __name__ == '__main__':
    host = '10.1.7.67'
    host2 = '10.1.7.83'
    port = 830
    login = 'root'
    password = 'netlabN.'
    config_file = 'test1_edit_config.xml'
    filter = "<transceiver/>"

    connectionTX = init_connection(host, port, login, password)
    create_configuration(connectionTX, config_file, 'running', 'merge', filter)
    close_connection(connectionTX)

    connectionRX = init_connection(host2, port, login, password)
    create_configuration(connectionRX, config_file, 'running', 'merge', filter)
    close_connection(connectionRX)
