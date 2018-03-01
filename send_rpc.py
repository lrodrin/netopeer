"""
This module send a RPC to the NETCONF server

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""

from ncclient.xml_ import to_ele

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

    rpc = '''
    <hello xmlns="urn:cttc:params:xml:ns:yang:test">
        <name>Laura</name>
    </hello>
    '''

    try:
        connection.dispatch(to_ele(rpc))

    except Exception as e:
        print(e)

    finally:
        connection.close_session()


if __name__ == '__main__':
    host = '10.1.7.84'
    port = 830
    login = 'root'
    password = 'netlabN.'

    execute_rpc(host, port, login, password)
