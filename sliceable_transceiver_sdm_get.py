"""
This module implements the measurement of the BANDWIDTH for slice 1

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""

import data as d


def get_bandwith_parameter(connection):
    try:

        template = """<transceiver xmlns="urn:sliceable-transceiver-sdm">
            <slice>
            <optical-signal><opticalchannelid>1</opticalchannelid><bandwidth></bandwidth></optical-signal>
            <optical-signal><opticalchannelid>2</opticalchannelid><bandwidth></bandwidth></optical-signal>
            <optical-signal><opticalchannelid>3</opticalchannelid><bandwidth></bandwidth></optical-signal>
            <optical-signal><opticalchannelid>4</opticalchannelid><bandwidth></bandwidth></optical-signal>
            <optical-signal><opticalchannelid>5</opticalchannelid><bandwidth></bandwidth></optical-signal>
            <optical-signal><opticalchannelid>6</opticalchannelid><bandwidth></bandwidth></optical-signal>
            <optical-signal><opticalchannelid>7</opticalchannelid><bandwidth></bandwidth></optical-signal>             
            </slice>
            </transceiver>"""

        print(d.get_config(connection, template, 'running'))

    except Exception as e:
        print(e)


if __name__ == '__main__':
    host = '10.1.7.84'
    port = 830
    login = 'root'
    password = 'netlabN.'

    connection = d.connect(host, port, login, password)
    get_bandwith_parameter(connection)
    connection.close_session()
