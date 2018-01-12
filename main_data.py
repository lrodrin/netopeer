"""
This module implements the main from data implementation

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""

import data as t

if __name__ == '__main__':
    connection = t.connect('10.1.7.81', 830, 'root', 'netlabN.')

    filter1 = '''<turing-machine xmlns="http://example.net/turing-machine">'''  # model turing-machine
    filter2 = '''<interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">'''  # model ietf-interfaces

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

    try:
        model = 'ietf-interfaces'
        # t.get_capabilities(connection)
        # t.get_capability(connection, model)
        # t.get_yang_schema(connection, model)

        # get_config
        #
        # print("running session:")
        # print(connection.get())
        # print("startup session:")
        # t.get_config(connection, filter1, session1)
        # t.get_config(connection, filter2, session1)
        print("running session:")
        t.get_config(connection, filter1, session2)
        t.get_config(connection, filter2, session2)
        # print("candidate session:")
        # t.get_config(connection, filter1, session3)
        # t.get_config(connection, filter2, session3)

        # edit-config datastore running
        #
        # TODO create subscription
        # t.edit_config(connection, edit_data, session2)
        t.edit_config(connection, edit_data2, session2)
        print("running session:")
        # t.get_config(connection, filter1, session2)
        t.get_config(connection, filter2, session2)

        # edit-config datastore candidate
        #
        # t.edit_config(connection, edit_data, session3)
        # t.edit_config(connection, edit_data2, session3)
        # print("candidate session:")
        # t.get_config(connection, filter1, session3)
        # t.get_config(connection, filter2, session3)

    finally:
        connection.close_session()
