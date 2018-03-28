"""
This module create the sliceable transceiver sdm configuration

Copyright (c) 2018-2019 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""

from lxml import etree

import kddi.data as d

# datastore sessions
session_startup = 'startup'
session_running = 'running'
session_candidate = 'candidate'

# NETCONF operations
operation_merge = 'merge'
operation_replace = 'replace'


def change_node_config(host, port, login, password, config_file, session, operation, filter):
    connection = d.connect(host, port, login, password)  # connection to NETCONF server

    # build xml
    config = etree.Element('config', xmlns="urn:ietf:params:xml:ns:netconf:base:1.0")
    transceiver = etree.SubElement(config, 'transceiver', xmlns="urn:sliceable-transceiver-sdm")
    slice = etree.SubElement(transceiver, 'slice')
    sliceid = etree.SubElement(slice, 'sliceid')
    channel = etree.SubElement(slice, "optical-channel")
    opticalchannelid = etree.SubElement(channel, 'opticalchannelid')
    coreid = etree.SubElement(channel, 'coreid').text = "Core19"
    modeid = etree.SubElement(channel, 'modeid')
    slot = etree.SubElement(channel, "frequency-slot")
    ncf = etree.SubElement(slot, "ncf").text = '41'
    width = etree.SubElement(slot, "slot-width").text = '2'

    try:
        d.edit_config(connection, config, session_running, operation_merge)
        print(d.get_config(connection, filter, session))


    except Exception as e:
        print(e)

    finally:
        connection.close_session()


if __name__ == '__main__':
    host = '10.1.7.67'
    port = 830
    login = 'root'
    password = 'netlabN.'
    config_file = 'slice1_add.xml'
    filter = "<transceiver/>"

    change_node_config(host, port, login, password, config_file, session_running, operation_merge, filter)
