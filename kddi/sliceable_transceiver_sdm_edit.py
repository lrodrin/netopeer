"""
This module implements the reconfiguration of the optical channels

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""

import kddi.data as d


def set_parameters(host, port, login, password, config_file, session, operation, filter):
    connection = d.connect(host, port, login, password)

    try:
        f = open(config_file)
        d.edit_config(connection, f.read(), session, operation)
        f.close()
        print("new sliceable-transceiver-sdm configuration created\nnew configuration:")
        print(d.get_config(connection, filter, session))

    except Exception as e:
        print(e)

    finally:
        connection.close_session()


if __name__ == '__main__':
    host = '10.1.7.83'
    port = 830
    login = 'root'
    password = 'netlabN.'
    config_file = 'test5_edit_config.xml'
    filter = "<transceiver/>"

    set_parameters(host, port, login, password, config_file, 'running', 'merge', filter)
