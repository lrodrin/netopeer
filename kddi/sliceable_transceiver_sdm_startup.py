"""
This module create the sliceable transceiver sdm configuration

Copyright (c) 2018-2019 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""

import data as d

# datastore sessions
session_startup = 'startup'
session_running = 'running'
session_candidate = 'candidate'

# NETCONF operations
operation_merge = 'merge'
operation_replace = 'replace'


def create_node_config(host, port, login, password, config_file, session, operation, namespace):
    connection = d.connect(host, port, login, password)  # connection to NETCONF server

    try:
        f = open(config_file)  # open configuration file
        d.edit_config(connection, f.read(), session, operation)  # create node configuration
        f.close()
        print("new sliceable-transceiver-sdm configuration created\nnew configuration:")
        d.get_config(connection, namespace, session)  # get node configuration

    except Exception as e:
        print(e)

    finally:
        connection.close_session()


if __name__ == '__main__':
    host = '10.1.7.67'
    port = 830
    login = 'root'
    password = 'netlabN.'
    config_file = 'slice1_add.xml'
    namespace = '''<transceiver xmlns="urn:sliceable-transceiver-sdm">'''

    create_node_config(host, port, login, password, config_file, session_running, operation_merge, namespace)
