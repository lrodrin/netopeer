"""
This module implements some code about the class ncclient, a NETCONF Python client

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""
import re
import xml.etree.ElementTree as ET

from ncclient import manager


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
    connection = manager.connect(host=host, port=port, username=username, password=password, hostkey_verify=False,
                                 device_params={'name': 'default'}, allow_agent=False, look_for_keys=False)
    return connection


def get_capabilities(connection):
    """
    Display the NETCONF server capabilities

    :param connection: connection
    """
    for capability in connection.server_capabilities:
        print(capability)


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
            print(server_capability)


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
    print(config)


def write_file(fi, fo):
    file = open(fo, "w")
    file.write(fi)
    file.close()


def edit_config(connection, data, session):
    """
    Edit the session config from the NETCONF server using edit-config operation

    :param connection: connection
    :param data: data
    :param session: datastore session
    :type data: str
    :type session: str
    """
    connection.edit_config(target=session, config=data)


def copy_config(connection, source_session, target_session):
    """
    Copy the configuration datastore from the NETCONF server to another configuration datastore

    :param connection: connection
    :param source_session: source datastore session
    :param target_session: target datastore session
    :type source_session: str
    :type target_session: str
    """
    connection.copy_config(source=source_session, target=target_session)


def lock_config(connection, session):
    """
    Lock the configuration for a session

    :param connection: connection
    :param session: datastore session
    :type session: str
    """
    connection.locked(target=session)


def unlock_config(connection, session):
    """

    :param connection: connection
    :param session: datastore session
    :type session: str
    """
    connection.unlock(target=session)
