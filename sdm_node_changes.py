"""
This module implements changes to the sdm_node configuration

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""

import sys

from bluespace import data as d

# datastore sessions
session_startup = 'startup'
session_running = 'running'
session_candidate = 'candidate'

# NETCONF operations
operation_merge = 'merge'
operation_replace = 'replace'


def change_signal_config(host, port, login, password, nodeid, portid, signalid, wavelength, mode):
    connection = d.connect(host, port, login, password)  # connection to NETCONF server

    namespace = '''<sdm_node xmlns="urn:cttc:params:xml:ns:yang:sdm_node">'''
    signal_config = '''
    <?xml version="1.0" encoding="UTF-8"?>
    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <sdm_node xmlns="urn:cttc:params:xml:ns:yang:sdm_node">
            <node-id>''' + nodeid + '''</node-id>
            <port>
                <port-id>''' + portid + '''</port-id>
                <signal>
                    <signal-id>''' + signalid + '''</signal-id>
                    <wavelength>''' + wavelength + '''</wavelength>
                    <mode>''' + mode + '''</mode>
                </signal>
            </port>
        </sdm_node>
    </config>
    '''

    try:
        d.edit_config(connection, signal_config, session_running, operation_replace)  # edit configuration
        print("node configuration edited\nnew configuration:")
        d.get_config(connection, namespace, session_running)  # get node configuration

    except Exception as e:
        print(e)

    finally:
        connection.close_session()


if __name__ == '__main__':
    if len(sys.argv) != 6:
        print("Usage: python sdm_node_changes.py [node-id] [port-id] [signal-id] [wavelength] [mode]")
        print("Example: python sdm_node_changes.py c 3000 3001 0 03")

    else:
        host = '10.1.7.84'
        port = 830
        login = 'root'
        password = 'netlabN.'

        change_signal_config(host, port, login, password, sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4],
                             sys.argv[5])
