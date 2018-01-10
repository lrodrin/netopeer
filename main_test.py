"""
This module implements the main from test class

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""

import test as t

if __name__ == '__main__':
    connection = t.connect('10.1.7.81', 830, 'root', 'netlabN.')

    filter1 = '''<turing-machine xmlns="http://example.net/turing-machine">'''
    filter2 = '''<interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">'''
    filter3 = '''<runaways xmlns="urn:opendaylight:params:xml:ns:yang:runaways"'''

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
                <name>eth0</name>
                <description>HE CANVIAT LA DESCRIPTION HEHE</description>
                <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd</type>
                <enabled>false</enabled>
            </interface>
        </interfaces>
    </config>
    '''

    edit_data3 = '''
    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
        <runaways xmlns="urn:opendaylight:params:xml:ns:yang:runaways">
                <hero>
                    <name>Karolina</name>                    
                    <description>Fly</description>
                </hero>
        </runaways>
    </config>
    '''

    try:
        model = 'runaways'
        # t.get_capabilities(connection)
        # t.get_capability(connection, model)
        # t.get_yang_schema(connection, model)

        # get_config
        # print("startup session:")
        # t.get_config(connection, filter1, session1)
        # print("running session:")
        # t.get_config(connection, filter1, session2)
        # print("candidate session:")
        # t.get_config(connection, filter1, session3)

        # edit-config
        t.edit_config(connection, edit_data, session3)
        print("candidate session:")
        t.get_config(connection, filter1, session3)
        print("running session:")
        t.get_config(connection, filter1, session2)

        # t.edit_config(connection, edit_data3, session3)
        # t.get_config(connection, filter3, session3)
        # t.copy_config(connection, session3, session2)
        # print("running session:")
        # t.get_config(connection, filter3, session2)

    finally:
        connection.close_session()
