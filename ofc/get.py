"""
This module implements ...

Copyright (c) 2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""
from ncclient import manager


def connect(host):
    try:
        connection = manager.connect(host=host, port=830, username='root', password='netlabN.', hostkey_verify=False,
                                     device_params={'name': 'default'}, allow_agent=False, look_for_keys=False)
        return connection

    except Exception as e:
        print(e)


if __name__ == '__main__':
    # hostTX = '10.1.7.65'
    hostRX = '10.1.7.66'
    # connectionTX = connect(hostTX)
    connectionRX = connect(hostRX)
