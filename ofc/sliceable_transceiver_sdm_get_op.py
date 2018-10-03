"""
This module implements the get_config steps for ofc

Copyright (c) 2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""
import xml.dom.minidom as md

from lxml import etree

import ofc.sliceable_transceiver_sdm_connection as connection

INDENT = ' ' * 4


def pretty_print(s):
    print('\n'.join(line for line in md.parseString(s).toprettyxml(indent=INDENT).split('\n') if line.strip()))


def generate_template(channels, start, end):
    transceiver = etree.Element('transceiver-connectivity', xmlns="urn:sliceable-transceiver-sdm-connectivity")
    slice = etree.SubElement(transceiver, 'slice')
    sliceid = etree.SubElement(slice, 'sliceid')
    sliceid.text = '1'
    for channel in range(start - 1, end):
        optical_signal = etree.SubElement(slice, 'optical-signal')
        opticalchannelid = etree.SubElement(optical_signal, 'opticalchannelid')
        opticalchannelid.text = str(channels[channel])
        monitor = etree.SubElement(optical_signal, 'monitor')
        etree.SubElement(monitor, 'osnr')
        etree.SubElement(monitor, 'ber')

    xml = etree.tostring(transceiver).decode()
    return xml


def get_step(conn, sess, template):
    try:
        config = conn.get_config(source=sess, filter=('subtree', template)).data_xml
        pretty_print(config)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    hostRX = '10.1.7.66'
    port = 830
    login = 'root'
    password = 'netlabN.'
    connectionRX = connection.connect(hostRX, port, login, password)
    session = 'running'
    channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    # STEP 1
    template = generate_template(channels, 1, 3)
    get_step(connectionRX, session, template)
    # STEP 2
    template = generate_template(channels, 1, 6)
    get_step(connectionRX, session, template)
    # STEP 3
    template = generate_template(channels, 1, 12)
    get_step(connectionRX, session, template)
    # STEP 5
    template = generate_template(channels, 7, 9)
    get_step(connectionRX, session, template)
    connection.close(connectionRX)
