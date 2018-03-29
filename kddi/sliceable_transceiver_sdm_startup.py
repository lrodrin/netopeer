"""
This module create the sliceable transceiver sdm configuration

Copyright (c) 2018-2019 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""

import kddi.data as d

# datastore sessions
session_startup = 'startup'
session_running = 'running'
session_candidate = 'candidate'

# NETCONF operations
operation_merge = 'merge'
operation_replace = 'replace'


def create_node_config(host, port, login, password, config_file, session, operation, filter):
    connection = d.connect(host, port, login, password)  # connection to NETCONF server

    try:
        f = open(config_file)  # open configuration file
        d.edit_config(connection, f.read(), session, operation)  # create sliceable transceiver sdm configuration
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
    config_file = 'test1_edit_config.xml'
    # config_file = 'test5_edit_config.xml'
    filter = "<transceiver/>"

    create_node_config(host, port, login, password, config_file, session_running, operation_merge, filter)
