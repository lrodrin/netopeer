"""
This module implements the reconfiguration of the optical channels

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""

import data as d


def set_parameters(connection, config_file, session, operation, filter):
    try:
        f = open(config_file)
        d.edit_config(connection, f.read(), session, operation)
        f.close()
        print(d.get_config(connection, filter, session))

    except Exception as e:
        print(e)


if __name__ == '__main__':
    host = '10.1.7.67'
    host2 = '10.1.7.83'
    port = 830
    login = 'root'
    password = 'netlabN.'
    config_file = 'test5_edit_config.xml'
    filter = "<transceiver/>"

    connectionTX = d.connect(host, port, login, password)
    set_parameters(connectionTX, config_file, 'running', 'merge', filter)
    connectionTX.close_session()

    connectionRX = d.connect(host2, port, login, password)
    set_parameters(connectionRX, config_file, 'running', 'merge', filter)
    connectionRX.close_session()
