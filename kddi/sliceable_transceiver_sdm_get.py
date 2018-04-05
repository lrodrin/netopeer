"""
This module implements the measurement of the OSNR and BER for slice 1

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""

import data as d


def get_ber_and_osnr_parameters(host, port, login, password):
    connection = d.connect(host, port, login, password)

    try:
        config = connection.get(
            filter='<nc:filter type="xpath" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" '
                   'xmlns:sliceable-transceiver-sdm="urn:sliceable-transceiver-sdm" '
                   'select="/sliceable-transceiver-sdm:transceiver-state"/>')

        # config = connection.get(
        #     filter='<nc:filter type="xpath" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" '
        #            'xmlns:ietf-interfaces="urn:ietf:params:xml:ns:yang:ietf-interfaces" '
        #            'select="/ietf-interfaces:interfaces-state"/interface>')

        print(config)

    except Exception as e:
        print(e)

    finally:
        connection.close_session()


if __name__ == '__main__':
    host = '10.1.7.83'
    port = 830
    login = 'root'
    password = 'netlabN.'

    get_ber_and_osnr_parameters(host, port, login, password)
