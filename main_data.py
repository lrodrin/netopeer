"""
This module implements the main from data implementation

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""

import data as t

if __name__ == '__main__':
    host = '10.1.7.81'
    port = 830
    connection = t.connect(host, port, 'root', 'netlabN.')  # connection to NETCONF server
    print('connected:', connection.connected, '.... to host', host, 'on port:', port)
    print('session-id:', connection.session_id)

    filter1 = '''<turing-machine xmlns="http://example.net/turing-machine">'''  # model turing-machine
    filter2 = '''<interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">'''  # model ietf-interfaces
    filter3 = '''<sdm-node xmlns="urn:cttc:params:xml:ns:yang:sdm-node">'''

    # datastore sessions
    session1 = 'startup'
    session2 = 'running'
    session3 = 'candidate'

    edit_data = '''
    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
        <turing-machine xmlns="http://example.net/turing-machine">
            <transition-function>
                <delta>
                    <label>left summand</label>
                    <input>
                        <state>10</state>
                        <symbol>1</symbol>
                    </input>
                </delta>
            </transition-function>
        </turing-machine>
    </config>
    '''

    edit_data2 = '''
    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>eth1</name>
                <description>Ethernet 1</description>
                <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd</type>
                <enabled>true</enabled>
                <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                    <enabled>true</enabled>
                    <mtu>1500</mtu>
                    <address>
                        <ip>8.8.8.8</ip>
                        <prefix-length>16</prefix-length>
                    </address>
                </ipv4>
            </interface>
        </interfaces>
    </config>
    '''

    edit_data3 = '''
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

    edit_data4 = '''
            <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
                <sdm-node xmlns="urn:cttc:params:xml:ns:yang:sdm-node">
                    <node-id>c</node-id>
                    <port>
                        <port-id>1000</port>
                        <signal>
                            <signal-id>0000</signal-id>
                            <wavelength>0</wavelength>
                            <mode>00</mode>
                        </signal>
                    </port>
                </sdm-node>
            </config>
        '''

    try:
        model = 'sdm-node'
        # print("server capabilities:")
        # t.get_capabilities(connection)
        # print("model %s capability:" % model)
        # t.get_capability(connection, model)

        # t.get_yang_schema(connection, model)
        # print("yang schema for model %s obtained" % model)

        # get_config
        #
        # print("get all:")
        # print(connection.get())

        # print("get startup session:")
        # t.get_config(connection, filter1, session1)
        # t.get_config(connection, filter2, session1)
        # t.get_config(connection, filter3, session1)

        print("get running session:")
        # t.get_config(connection, filter1, session2)
        # t.get_config(connection, filter2, session2)
        t.get_config(connection, filter3, session2)

        # print("get candidate session:")
        # t.get_config(connection, filter1, session3)
        # t.get_config(connection, filter2, session3)
        # t.get_config(connection, filter3, session3)

        # edit-config datastore running
        #
        print("edit running session")
        # t.edit_config(connection, edit_data, session2)
        # t.edit_config(connection, edit_data2, session2)
        t.edit_config(connection, edit_data3, session2)
        print("get running session:")
        # t.get_config(connection, filter1, session2)
        # t.get_config(connection, filter2, session2)
        t.get_config(connection, filter3, session2)

        print("edit running session")
        t.edit_config(connection, edit_data4, session2)
        print("get running session:")
        t.get_config(connection, filter3, session2)

        # edit-config datastore candidate
        #
        # print("edit candidate session")
        # t.edit_config(connection, edit_data, session3)
        # t.edit_config(connection, edit_data2, session3)
        # t.edit_config(connection, edit_data3, session3)
        # print("get candidate session:")
        # t.get_config(connection, filter1, session3)
        # t.get_config(connection, filter2, session3)
        # t.get_config(connection, filter3, session3)

    finally:
        connection.close_session()
