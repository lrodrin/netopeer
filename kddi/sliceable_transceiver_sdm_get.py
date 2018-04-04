"""
This module implements the measurement of the OSNR and BER for slice 1

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""

import data as d


def get_ber_and_osnr_parameters(host, port, login, password):
    connection = d.connect(host, port, login, password)

    template = """<transceiver xmlns="urn:sliceable-transceiver-sdm">
        <slice><optical-signal><opticalchannelid>1</opticalchannelid><monitor><ber></ber><osnr></osnr></monitor></optical-signal>
        <optical-signal><opticalchannelid>2</opticalchannelid><monitor><ber></ber><osnr></osnr></monitor></optical-signal>
        <optical-signal><opticalchannelid>3</opticalchannelid><monitor><ber></ber><osnr></osnr></monitor></optical-signal>
        <optical-signal><opticalchannelid>4</opticalchannelid><monitor><ber></ber><osnr></osnr></monitor></optical-signal>
        <optical-signal><opticalchannelid>5</opticalchannelid><monitor><ber></ber><osnr></osnr></monitor></optical-signal>
        <optical-signal><opticalchannelid>6</opticalchannelid><monitor><ber></ber><osnr></osnr></monitor></optical-signal>
        </slice>
        </transceiver>"""

    template2 = """<interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface><name>eth0</name></interface>
        </interfaces/>"""

    try:
        config = connection.get_config(source='running', filter=('subtree', template2))
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
