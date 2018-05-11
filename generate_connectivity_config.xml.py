"""
This module generate node connectivity XML configuration

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""

from lxml import etree

from data import pretty_print


def generate(filename, id_connection, id_port_in, id_port_out, id_transceiver):
    config = etree.Element('config', xmlns="urn:ietf:params:xml:ns:netconf:base:1.0")
    connection = etree.SubElement(config, 'connection', xmlns="urn:node-connectivity")
    connectionid = etree.SubElement(connection, 'connectionid')
    connectionid.text = '%s' % id_connection
    port_in_id = etree.SubElement(connection, 'port-in_id')
    port_in_id.text = '%s' % id_port_in
    port_out_id = etree.SubElement(connection, 'port-out_out')
    port_out_id.text = '%s' % id_port_out
    transceiverid = etree.SubElement(connection, 'transceiverid')
    transceiverid.text = '%s' % id_transceiver

    xml = etree.tostring(config)
    pretty_xml = pretty_print(xml)
    with open(filename, "w") as f:
        f.write(pretty_xml)


if __name__ == '__main__':
    generate("node_connectivity_config.xml", 1, 1, 1, 1)
