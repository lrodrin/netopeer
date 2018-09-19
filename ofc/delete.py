"""
This module delete the running configuration of slice 1

Copyright (c) 2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""

import kddi.data as d


def init_connection(host, port, login, password):
    connection = d.connect(host, port, login, password)
    return connection


def delete_configuration(connection, session):
    try:
        template = """<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <transceiver-connectivity xmlns="urn:sliceable-transceiver-sdm-connectivity">
                <slice>
                    <sliceid>1</sliceid>
                </slice>
            </transceiver-connectivity>
        </config>"""
        connection.edit_config(target=session, config=template, default_operation='replace')

    except Exception as e:
        print(e)


def close_connection(connection):
    connection.close_session()


if __name__ == '__main__':
    hostRX = '10.1.7.66'
    port = 830
    login = 'root'
    password = 'netlabN.'

    connectionTX = init_connection(hostTX, port, login, password)
    delete_configuration(connectionTX, 'running')
    close_connection(connectionTX)

    connectionRX = init_connection(hostRX, port, login, password)
    delete_configuration(connectionRX, 'running')
    close_connection(connectionRX)
