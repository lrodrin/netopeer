"""
This module create the configuration of one spectral super channel (slice)

Copyright (c) 2018-2019 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""

import data as d


def create_configuration(host, port, login, password, config_file, session, operation, filter):
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
    host2 = '10.1.7.83'
    port = 830
    login = 'root'
    password = 'netlabN.'
    config_file = 'test1_edit_config.xml'
    filter = "<transceiver/>"

    create_configuration(host, port, login, password, config_file, 'running', 'merge', filter)
    create_configuration(host2, port, login, password, config_file, 'running', 'merge', filter)
