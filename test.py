"""
This module implements some code about the class ncclient, a NETCONF Python client

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""
from ncclient import manager
import xml.etree.ElementTree as ET


def connect(host):
    """
    Connection to NETCONF server

    :param host: ip address
    :type host: str
    :return: c
    """
    c = manager.connect(host=host, port=830, username='root', password='netlabN.', hostkey_verify=False,
                        device_params={'name': 'csr'})  # support the device handler Cisco CSR
    return c


def get_capabilities(c):
    """
    Display the NETCONF server capabilities
    
    :param c: connection
    """
    for capability in c.server_capabilities:
        print(capability)


def get_yang_schema(c, yang_model):
    """
    Obtain a YANG model specified by yang_model and write it into a file

    :param c: connection
    :param yang_model: yang model
    :type yang_model: str
    """
    schema = c.get_schema(yang_model)
    root = ET.fromstring(schema.xml)
    yang_text = list(root)[0].text
    write_file(yang_text, yang_model + ".yang")


def get_config(c):
    """
    Retrieve the running config from the NETCONF server using get-config and write the XML config to a file

    :param c: connection
    """
    file = c.get_config(source='running').data_xml
    write_file(file, "get_config.xml")


def write_file(fi, fo):
    f = open(fo, "w")
    f.write(fi)
    f.close()


def edit_config(c):
    """
    Edit the running config from the NETCONF server using edit-config and write the XML config to a file

    :param c: connection
    """
    template = """<input xmlns="urn:opendaylight:params:xml:ns:yang:hello">
    <name>Laura</name></input>"""

    file = c.edit_config(target='running', config=template).data_xml
    write_file(file, "edit_config.xml")


if __name__ == '__main__':
    ip_address = '10.1.7.81'
    connection = connect(ip_address)
    try:
        # get_capabilities(connection)
        get_yang_schema(connection, 'hello')
        # get_config(connection)
        # edit_config(connection)
    finally:
        connection.close_session()
