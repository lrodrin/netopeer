"""
This module create the configuration for test1, test2 and tes3

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
    test_config_files = ['test1.xml', 'test2.xml', 'test3.xml']
    filter = "<transceiver-connectivity/>"

    for config_file in test_config_files:
        connectionTX = init_connection(host, port, login, password)
        create_configuration(connectionTX, config_file, 'running', 'merge', filter)
        close_connection(connectionTX)

        connectionRX = init_connection(host2, port, login, password)
        create_configuration(connectionRX, config_file, 'running', 'merge', filter)
        close_connection(connectionRX)
