"""
This module executes a RPC

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""

import data as d

# datastore sessions
session_startup = 'startup'
session_running = 'running'
session_candidate = 'candidate'

# NETCONF operations
operation_merge = 'merge'
operation_replace = 'replace'


def execute_rpc(host, port, login, password):
    connection = d.connect(host, port, login, password)  # connection to NETCONF server

    rpc = ''''
    <turing-machine xmlns="http://example.net/turing-machine">
        <run-until>
            <state>1</state>
            <head-position>1</head-position>
        </run-until>
    </turing-machine>
    '''

    try:
        connection.rpc(rpc)
        connection.execute(rpc)

    except Exception as e:
        print(e)

    finally:
        connection.close_session()


if __name__ == '__main__':
    host = '10.1.7.81'
    port = 830
    login = 'root'
    password = 'netlabN.'

    execute_rpc(host, port, login, password)
