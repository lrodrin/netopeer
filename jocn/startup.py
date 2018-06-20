"""
This module create the configuration of one spectral super channel (slice)

Copyright (c) 2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""

import kddi.data as d


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
    host = '10.1.7.65'
    host2 = '10.1.7.66'
    port = 830
    login = 'root'
    password = 'netlabN.'
    test1_config_file = 'test1.xml'
    filter = "<transceiver-connectivity/>"

    connectionTX = init_connection(host, port, login, password)
    create_configuration(connectionTX, test1_config_file, 'running', 'merge', filter)
    close_connection(connectionTX)

    # connectionRX = init_connection(host2, port, login, password)
    # create_configuration(connectionRX, test1_config_file, 'running', 'merge', filter)
    # close_connection(connectionRX)
