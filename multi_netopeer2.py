"""
This module implements the client who manage three netopeer2 servers in one machine

Copyright (c) 2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""
import xml.dom.minidom as md

from ncclient import manager

INDENT = ' ' * 4


def connect_to_multi_netopeer2(port):
    try:
        connection = manager.connect(host='10.1.7.83', port=port, username='root', password='netlabN.',
                                     hostkey_verify=False,
                                     device_params={'name': 'default'}, allow_agent=False, look_for_keys=False)
        return connection

    except Exception as e:
        print(e)


def create_node_configuration(connection, config_file):
    try:
        file = open(config_file)
        connection.edit_config(target='running', config=file.read(), default_operation='merge')
        file.close()

    except Exception as e:
        print(e)


def get(connection, nodeid, portid):
    try:
        template = '''
        <node xmlns="urn:node-topology">
            <node-id>''' + nodeid + '''</node-id>
            <port>
                <port-id>''' + portid + '''</port-id>
            </port>
        </node>'''

        config = connection.get_config(source='running', filter=('subtree', template)).data_xml
        print(pretty_print(config))

    except Exception as e:
        print(e)


def pretty_print(s):
    return '\n'.join(line for line in md.parseString(s).toprettyxml(indent=INDENT).split('\n') if line.strip())


def edit(connection, nodeid, portid, layer_protocol_name):
    try:
        template = '''
        <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <node xmlns="urn:node-topology">
                <node-id>''' + nodeid + '''</node-id>
                <port>
                    <port-id>''' + portid + '''</port-id>
                    <layer-protocol-name> ''' + layer_protocol_name + '''</layer-protocol-name>
                </port>
            </node>
        </config>'''

        connection.edit_config(target='running', config=template, default_operation='merge')

    except Exception as e:
        print(e)


def delete(connection, nodeid):
    try:
        template = '''
        <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <node xmlns="urn:node-topology">
                <node-id>''' + nodeid + '''</node-id>
            </node>
        </config>'''

        connection.edit_config(target='running', config=template, default_operation='replace')

    except Exception as e:
        print(e)


if __name__ == '__main__':
    # startup
    config_file_65 = 'node_topology_config_65.xml'
    connection_65 = connect_to_multi_netopeer2(831)
    create_node_configuration(connection_65, config_file_65)

    config_file_66 = 'node_topology_config_66.xml'
    connection_66 = connect_to_multi_netopeer2(832)
    create_node_configuration(connection_66, config_file_66)

    config_file_67 = 'node_topology_config_67.xml'
    connection_67 = connect_to_multi_netopeer2(833)
    create_node_configuration(connection_67, config_file_67)

    # test1 - get parameters from node 10.1.7.65 and port id 3
    print("TEST 1: GET")
    get(connection_65, '10.1.7.65', '3')
    # test2 - edit layer-protocol-name from node 10.1.7.66 and port id 4
    print("TEST 2: EDIT")
    edit(connection_66, '10.1.7.66', '4', 'sdm')
    get(connection_66, '10.1.7.66', '4')
    # test3 - deletel node 10.1.7.67 configuration
    print("TEST 3: DELETE")
    delete(connection_66, '10.1.7.67')

    # close
    connection_65.close_session()
    connection_66.close_session()
    connection_67.close_session()
