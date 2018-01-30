"""
This module create the node configuration

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""

import data as t

if __name__ == '__main__':
    host = '10.1.7.81'
    port = 830
    connection = t.connect(host, port, 'root', 'netlabN.')  # connection to NETCONF server

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
                <port-id>1000</port-id>
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
                <port-id>2000</port-id>
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
                <port-id>3000</port-id>
                <signal>
                    <signal-id>3001</signal-id>
                    <wavelength>3</wavelength>
                    <mode>03</mode>
                </signal>
            </port>
        </sdm-node>
    </config>
    '''

    try:
        t.edit_config(connection, edit_data, session2, operation1)  # create node configuration
        print("new node configuration created\nnew configuration:")
        t.get_config(connection, filter, session2)  # get node configuration

    except Exception as e:
        print(e)

    finally:
        connection.close_session()
