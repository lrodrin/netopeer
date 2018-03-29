"""
This module implements ...

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""

import kddi.data as d


def get_interface_state(host, port, login, password):
    connection = d.connect(host, port, login, password)

    # template = """<transceiver xmlns="urn:sliceable-transceiver-sdm">
    #     <slice><optical-signal><opticalchannelid>%s</opticalchannelid><monitor><ber></ber><osnr></osnr></monitor></optical-signal></slice>
    #     </transceiver>"""
    #
    # for i in range(0, 7):
    #     config = connection.get_config(source='running', filter=('subtree', template % str(i)))
    #     print(config)

    template = """<transceiver xmlns="urn:sliceable-transceiver-sdm">
        <slice><optical-signal><opticalchannelid>1</opticalchannelid><monitor><ber></ber><osnr></osnr></monitor></optical-signal>
        <optical-signal><opticalchannelid>2</opticalchannelid><monitor><ber></ber><osnr></osnr></monitor></optical-signal>
        <optical-signal><opticalchannelid>3</opticalchannelid><monitor><ber></ber><osnr></osnr></monitor></optical-signal>
        <optical-signal><opticalchannelid>4</opticalchannelid><monitor><ber></ber><osnr></osnr></monitor></optical-signal>
        <optical-signal><opticalchannelid>5</opticalchannelid><monitor><ber></ber><osnr></osnr></monitor></optical-signal>
        <optical-signal><opticalchannelid>6</opticalchannelid><monitor><ber></ber><osnr></osnr></monitor></optical-signal>
        </slice>
        </transceiver>"""

    config = connection.get_config(source='running', filter=('subtree', template))
    print(config)


if __name__ == '__main__':
    host = '10.1.7.83'
    port = 830
    login = 'root'
    password = 'netlabN.'
    get_interface_state(host, port, login, password)
