"""
This module implements change the node configuration

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
        t.edit_config(connection, edit_data, session2, operation2)  # edit configuration
        print("node configuration edited\nnew configuration:")
        t.get_config(connection, filter, session2)

    finally:
        connection.close_session()
