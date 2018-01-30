"""
This module implements a test from data implementation

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""

import data as t

if __name__ == '__main__':
    host = '10.1.7.81'
    port = 830
    connection = t.connect(host, port, 'root', 'netlabN.')  # connection to NETCONF server
    print('server connected:', connection.connected, '.... to host', host, 'on port:', port)
    print('session-id:', connection.session_id)

    filter = '''<sdm-node xmlns="urn:cttc:params:xml:ns:yang:sdm-node">'''

    # datastore sessions
    session1 = 'startup'
    session2 = 'running'
    session3 = 'candidate'

    # operations
    operation1 = 'merge'
    operation2 = 'replace'

    edit_data = '''
    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
        <sdm-node xmlns="urn:cttc:params:xml:ns:yang:sdm-node">
            <node-id>a</node-id>
            <port>
                <port-id>1000</port>
                <signal>
                    <signal-id>1001</signal-id>
                    <wavelength>1</wavelength>
                    <mode>01</mode>
                </signal>
            </port>
        </sdm-node>
        <sdm-node xmlns="urn:cttc:params:xml:ns:yang:sdm-node">
            <node-id>b</node-id>
            <port>
                <port-id>2000</port>
                <signal>
                    <signal-id>2001</signal-id>
                    <wavelength>2</wavelength>
                    <mode>02</mode>
                </signal>
            </port>
        </sdm-node>
        <sdm-node xmlns="urn:cttc:params:xml:ns:yang:sdm-node">
            <node-id>c</node-id>
            <port>
                <port-id>3000</port>
                <signal>
                    <signal-id>3001</signal-id>
                    <wavelength>3</wavelength>
                    <mode>03</mode>
                </signal>
            </port>
        </sdm-node>
    </config>
    '''

    edit_data2 = '''
    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
        <sdm-node xmlns="urn:cttc:params:xml:ns:yang:sdm-node">
            <node-id>c</node-id>
            <port>
                <port-id>3000</port>
                <signal>
                    <signal-id>3001</signal-id>
                    <wavelength>0</wavelength>
                    <mode>03</mode>
                </signal>
            </port>
        </sdm-node>
    </config>
    '''

    try:

        # get-config
        #
        print("get config from startup session:")
        t.get_config(connection, filter, session1)

        print("get config from running session:")
        t.get_config(connection, filter, session2)

        # edit-config
        #
        # t.edit_config(connection, edit_data, session2, operation1)    # create configuration
        # t.edit_config(connection, edit_data2, session2, operation2)   # edit configuration

    finally:
        connection.close_session()
