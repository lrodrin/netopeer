"""
This module implements configuration methods to manipulate a NETCONF server

Copyright (c) 2018-2019 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""
import re
import xml.dom.minidom as md
import xml.etree.ElementTree as ET

import six
from ncclient import manager

INDENT = ' ' * 4


def connect(host, port, username, password):
    """
    Connection to NETCONF server


    :param host: ip address
    :param port: port number
    :param username: user name
    :param password: password for username
    :type host: str
    :type port: int
    :type username: str
    :type password: str
    :return: connection object
    """
    try:
        connection = manager.connect(host=host, port=port, username=username, password=password, hostkey_verify=False,
                                     device_params={'name': 'default'}, allow_agent=False, look_for_keys=False)
        six.print_('server connected to host ', host, ' on port:', port)
        six.print_('session-id:', connection.session_id)
        return connection

    except Exception as e:
        six.print_(e)


def get_capabilities(connection):
    """
    Display the NETCONF server capabilities

    :param connection: connection
    """
    for capability in connection.server_capabilities:
        six.print_(capability)


def get_capability(connection, model_name):
    """
    Display the capability from a model specified by model_name

    :param connection: connection
    :param model_name: model
    :type model_name: str
    :return: capability for model_name
    """
    for server_capability in connection.server_capabilities:
        model = re.search(model_name, server_capability)
        if model is not None:
            six.print_(server_capability)


def get_yang_schema(connection, yang_model):
    """
    Obtain a YANG model specified by yang_model and write it into a file

    :param connection: connection
    :param yang_model: yang model
    :type yang_model: str
    """
    schema = connection.get_schema(yang_model)
    aux = ET.fromstring(schema.xml)
    yang_text = list(aux)[0].text
    write_file(yang_text, yang_model + ".yang")


def get_config(connection, filter, session):
    """
    Retrieve the session config from the NETCONF server using a get-config operation

    :param connection: connection
    :param filter: filter
    :param session: datastore session
    :type session: str
    :type filter: str
    """
    config = connection.get_config(source=session, filter=('subtree', filter)).data_xml
    pretty_print(config)


def write_file(fi, fo):
    file = open(fo, "w")
    file.write(fi)
    file.close()


def edit_config(connection, data, session, operation):
    """
    Edit the session config from the NETCONF server using edit-config operation

    :param connection: connection
    :param data: data
    :param session: datastore session
    :param operation: merge, replace or nonne
    :type data: str
    :type session: str
    :type operation: str
    """
    connection.edit_config(target=session, config=data, default_operation=operation)


def pretty_print(filename):
    """
    Pretty print for XML specified by filename

    :param filename: file name
    :type filename: file
    """
    six.print_(
        '\n'.join(line for line in md.parseString(filename).toprettyxml(indent=INDENT).split('\n') if line.strip()))
