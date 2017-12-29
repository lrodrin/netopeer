"""
This module implements the main from test class

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""

import test as t

if __name__ == '__main__':
    ip_address = '10.1.7.81'
    connection = t.connect(ip_address)

    f1 = '''<turing-machine xmlns="http://example.net/turing-machine">'''
    f2 = '''<interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">'''
    f3 = '''<toaster xmlns="http://netconfcentral.org/ns/toaster"/>'''

    edit_data = """<config xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
    <turing-machine xmlns="http://example.net/turing-machine">
        <transition-function> 
            <delta> 
                <label>left summand</label> 
                    <input nc:operation="replace">
                        <state>10</state>
                        <symbol>11</symbol>
                    </input>      
            </delta>
        </transition-function>
    </turing-machine></config>"""

    try:
        # t.get_capabilities(connection)
        # t.get_capability(connection, 'hello')
        # t.get_yang_schema(connection, 'hello')
        t.get_config(connection, f1)
        t.get_config(connection, f2)
        t.get_config(connection, f3)
        # t.edit_config(connection, edit_data)

    finally:
        connection.close_session()
