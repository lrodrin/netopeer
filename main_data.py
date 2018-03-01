"""
This module implements the main test of configuration methods to manipulate a NETCONF server

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""

from bluespace import data as t

if __name__ == '__main__':
    host = '10.1.7.84'
    port = 830
    connection = t.connect(host, port, 'root', 'netlabN.')  # connection to NETCONF server

    filter1 = '''<turing-machine xmlns="http://example.net/turing-machine">'''  # model turing-machine
    filter2 = '''<interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">'''  # model ietf-interfaces
    filter3 = '''<sdm_node xmlns="urn:cttc:params:xml:ns:yang:sdm_node">'''  # model sdm_node

    # datastore sessions
    session_startup = 'startup'
    session_running = 'running'
    session_candidate = 'candidate'

    # operations
    operation_merge = 'merge'
    operation_replace = 'replace'

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
            <sdm_node xmlns="urn:cttc:params:xml:ns:yang:sdm_node">
                <node-id>a</node-id>
                <port>
                    <port-id>1000</port>
                    <signal>
                        <signal-id>1001</signal-id>
                        <wavelength>1</wavelength>
                        <mode>01</mode>
                    </signal>
                </port>
            </sdm_node>
            <sdm_node xmlns="urn:cttc:params:xml:ns:yang:sdm_node">
                <node-id>b</node-id>
                <port>
                    <port-id>2000</port>
                    <signal>
                        <signal-id>2001</signal-id>
                        <wavelength>2</wavelength>
                        <mode>02</mode>
                    </signal>
                </port>
            </sdm_node>
            <sdm_node xmlns="urn:cttc:params:xml:ns:yang:sdm_node">
                <node-id>c</node-id>
                <port>
                    <port-id>3000</port>
                    <signal>
                        <signal-id>3001</signal-id>
                        <wavelength>3</wavelength>
                        <mode>03</mode>
                    </signal>
                </port>
            </sdm_node>
        </config>
        '''

    edit_data4 = '''
            <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
                <sdm_node xmlns="urn:cttc:params:xml:ns:yang:sdm_node">
                    <node-id>c</node-id>
                    <port>
                        <port-id>3000</port>
                        <signal>
                            <signal-id>3001</signal-id>
                            <wavelength>0</wavelength>
                            <mode>03</mode>
                        </signal>
                    </port>
                </sdm_node>
            </config>
        '''

    try:
        model = 'sdm_node'
        print("server capabilities:")
        t.get_capabilities(connection)

        print("model %s capability:" % model)
        t.get_capability(connection, model)

        t.get_yang_schema(connection, model)
        print("yang schema for model %s obtained" % model)

        # get_config
        print("get all:")
        print(connection.get())

        print("get startup session:")
        t.get_config(connection, filter1, session_startup)
        t.get_config(connection, filter2, session_startup)
        t.get_config(connection, filter3, session_startup)

        print("get running session:")
        t.get_config(connection, filter1, session_running)
        t.get_config(connection, filter2, session_running)
        t.get_config(connection, filter3, session_running)

        print("get candidate session:")
        t.get_config(connection, filter1, session_candidate)
        t.get_config(connection, filter2, session_candidate)
        t.get_config(connection, filter3, session_candidate)

        # edit-config
        #
        print("edit running session")
        t.edit_config(connection, edit_data, session_running, operation_merge)
        t.edit_config(connection, edit_data2, session_running, operation_merge)
        t.edit_config(connection, edit_data3, session_running, operation_merge)
        t.edit_config(connection, edit_data4, session_running, operation_merge)

        t.edit_config(connection, edit_data, session_running, operation_replace)
        t.edit_config(connection, edit_data2, session_running, operation_replace)
        t.edit_config(connection, edit_data3, session_running, operation_replace)
        t.edit_config(connection, edit_data4, session_running, operation_replace)

        print("edit candidate session")
        t.edit_config(connection, edit_data, session_candidate, operation_merge)
        t.edit_config(connection, edit_data2, session_candidate, operation_merge)
        t.edit_config(connection, edit_data3, session_candidate, operation_merge)
        t.edit_config(connection, edit_data4, session_candidate, operation_merge)

        t.edit_config(connection, edit_data, session_candidate, operation_replace)
        t.edit_config(connection, edit_data2, session_candidate, operation_replace)
        t.edit_config(connection, edit_data3, session_candidate, operation_replace)
        t.edit_config(connection, edit_data4, session_candidate, operation_replace)

    finally:
        connection.close_session()
