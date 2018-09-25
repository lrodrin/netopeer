"""
This module implements the SSH connection to NETCONF servers TX and RX

Copyright (c) 2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""
from ncclient import manager


def connect(host, port, login, password):
    try:
        connection = manager.connect(host=host, port=port, username=login, password=password, hostkey_verify=False,
                                     device_params={'name': 'default'}, allow_agent=False, look_for_keys=False)
        print('Server connected to host:', host, 'on port:', port)
        return connection

    except Exception as e:
        print(e)


def close(connection):
    connection.close_session()
