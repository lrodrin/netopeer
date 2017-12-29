"""
This module implements some code about the class ncclient, a NETCONF Python client

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""
import re
import xml.etree.ElementTree as ET

from ncclient import manager


def connect(host):
    """
    Connection to NETCONF server

    :param host: ip address
    :type host: str
    :return: c
    """
    c = manager.connect(host=host, port=830, username='root', password='netlabN.', hostkey_verify=False,
                        device_params={'name': 'default'}, allow_agent=False,
                        look_for_keys=False)  # support the device handler Cisco CSR
    return c


def get_capabilities(c):
    """
    Display the NETCONF server capabilities
    
    :param c: connection
    """
    for capability in c.server_capabilities:
        print(capability)


def get_capability(c, m):
    """
    Display the capability from a model specified by m

    :param c: connection
    :param m: model
    :type m: str
    :return: capability
    """
    for sc in c.server_capabilities:
        model = re.search(m, sc)
        if model is not None:
            print(sc)


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


def get_config(c, f):
    """
    Retrieve the running config from the NETCONF server using get-config and write the XML config to a file

    :param f: filter
    :param c: connection
    """
    config = c.get_config(source='startup', filter=('subtree', f)).data_xml
    print(config)


def write_file(fi, fo):
    f = open(fo, "w")
    f.write(fi)
    f.close()


def edit_config(c, data):
    """
    Edit the running config from the NETCONF server using edit-config and write the XML config to a file

    :param c: connection
    :param data: data
    """
    c.locked(target='running')
    c.edit_config(target='running', config=data)
    c.commit()
