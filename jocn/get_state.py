"""
This module implements the measurement of the OSNR and BER for slice 1

Copyright (c) 2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""

import kddi.data as d


def init_connection(host, port, login, password):
    connection = d.connect(host, port, login, password)
    return connection


def get_ber_and_osnr_parameters(connection):
    try:
        config = connection.get(
            filter='<nc:filter type="xpath" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" '
                   'xmlns:sliceable-transceiver-sdm-connectivity="urn:sliceable-transceiver-sdm-connectivity" '
                   'select="/sliceable-transceiver-sdm-connectivity:transceiver-connectivity-state"/>')

        print(d.pretty_print(config.xml))

    except Exception as e:
        print(e)


def close_connection(connection):
    connection.close_session()


if __name__ == '__main__':
    hostRX = '10.1.7.66'
    port = 830
    login = 'root'
    password = 'netlabN.'

    connectionRX = init_connection(hostRX, port, login, password)
    get_ber_and_osnr_parameters(connectionRX)
    close_connection(connectionRX)
