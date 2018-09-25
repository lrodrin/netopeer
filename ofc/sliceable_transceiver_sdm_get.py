"""
This module implements the get_config steps for ofc

Copyright (c) 2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""
import xml.dom.minidom as md

import ofc.sliceable_transceiver_sdm_connection as connection

INDENT = ' ' * 4


def pretty_print(s):
    print('\n'.join(line for line in md.parseString(s).toprettyxml(indent=INDENT).split('\n') if line.strip()))


test = "<optical-channel><opticalchannelid>7</opticalchannelid><coreid></coreid><modeid></modeid></optical-channel>"


def get_step_1(conn, sess):
    try:
        template = """<transceiver-connectivity xmlns="urn:sliceable-transceiver-sdm-connectivity">
        <slice>
        <sliceid>1</sliceid>                
        <optical-signal><opticalchannelid>1</opticalchannelid><monitor><osnr></osnr><ber></ber></monitor></optical-signal>
        <optical-signal><opticalchannelid>2</opticalchannelid><monitor><osnr></osnr><ber></ber></monitor></optical-signal>
        <optical-signal><opticalchannelid>3</opticalchannelid><monitor><osnr></osnr><ber></ber></monitor></optical-signal>
        </slice>
        </transceiver-connectivity>"""

        config = conn.get_config(source=sess, filter=('subtree', template)).data_xml
        pretty_print(config)

    except Exception as e:
        print(e)


def get_step_2(conn, sess):
    try:
        template = """<transceiver-connectivity xmlns="urn:sliceable-transceiver-sdm-connectivity">
        <slice>
        <sliceid>1</sliceid>                
        <optical-signal><opticalchannelid>1</opticalchannelid><monitor><osnr></osnr><ber></ber></monitor></optical-signal>
        <optical-signal><opticalchannelid>2</opticalchannelid><monitor><osnr></osnr><ber></ber></monitor></optical-signal>
        <optical-signal><opticalchannelid>3</opticalchannelid><monitor><osnr></osnr><ber></ber></monitor></optical-signal>
        <optical-signal><opticalchannelid>4</opticalchannelid><monitor><osnr></osnr><ber></ber></monitor></optical-signal>
        <optical-signal><opticalchannelid>5</opticalchannelid><monitor><osnr></osnr><ber></ber></monitor></optical-signal>
        <optical-signal><opticalchannelid>6</opticalchannelid><monitor><osnr></osnr><ber></ber></monitor></optical-signal>
        </slice>
        </transceiver-connectivity>"""

        config = conn.get_config(source=sess, filter=('subtree', template)).data_xml
        pretty_print(config)

    except Exception as e:
        print(e)


def get_step_3(conn, sess):
    try:
        template = """<transceiver-connectivity xmlns="urn:sliceable-transceiver-sdm-connectivity">
        <slice>
        <sliceid>1</sliceid>                
        <optical-signal><opticalchannelid>1</opticalchannelid><monitor><osnr></osnr><ber></ber></monitor></optical-signal>
        <optical-signal><opticalchannelid>2</opticalchannelid><monitor><osnr></osnr><ber></ber></monitor></optical-signal>
        <optical-signal><opticalchannelid>3</opticalchannelid><monitor><osnr></osnr><ber></ber></monitor></optical-signal>
        <optical-signal><opticalchannelid>4</opticalchannelid><monitor><osnr></osnr><ber></ber></monitor></optical-signal>
        <optical-signal><opticalchannelid>5</opticalchannelid><monitor><osnr></osnr><ber></ber></monitor></optical-signal>
        <optical-signal><opticalchannelid>6</opticalchannelid><monitor><osnr></osnr><ber></ber></monitor></optical-signal>
        <optical-signal><opticalchannelid>7</opticalchannelid><monitor><osnr></osnr><ber></ber></monitor></optical-signal>
        <optical-signal><opticalchannelid>8</opticalchannelid><monitor><osnr></osnr><ber></ber></monitor></optical-signal>
        <optical-signal><opticalchannelid>9</opticalchannelid><monitor><osnr></osnr><ber></ber></monitor></optical-signal>
        <optical-signal><opticalchannelid>10</opticalchannelid><monitor><osnr></osnr><ber></ber></monitor></optical-signal>
        <optical-signal><opticalchannelid>11</opticalchannelid><monitor><osnr></osnr><ber></ber></monitor></optical-signal>
        <optical-signal><opticalchannelid>12</opticalchannelid><monitor><osnr></osnr><ber></ber></monitor></optical-signal>
        </slice>
        </transceiver-connectivity>"""

        config = conn.get_config(source=sess, filter=('subtree', template)).data_xml
        pretty_print(config)

    except Exception as e:
        print(e)


def get_step_4(conn, sess):
    try:
        template = """<transceiver-connectivity xmlns="urn:sliceable-transceiver-sdm-connectivity">
        <slice>
        <sliceid>1</sliceid>                
        <optical-signal><opticalchannelid>1</opticalchannelid><monitor><osnr></osnr><ber></ber></monitor></optical-signal>
        <optical-signal><opticalchannelid>2</opticalchannelid><monitor><osnr></osnr><ber></ber></monitor></optical-signal>
        <optical-signal><opticalchannelid>3</opticalchannelid><monitor><osnr></osnr><ber></ber></monitor></optical-signal>
        <optical-signal><opticalchannelid>7</opticalchannelid><monitor><osnr></osnr><ber></ber></monitor></optical-signal>
        <optical-signal><opticalchannelid>8</opticalchannelid><monitor><osnr></osnr><ber></ber></monitor></optical-signal>
        <optical-signal><opticalchannelid>9</opticalchannelid><monitor><osnr></osnr><ber></ber></monitor></optical-signal>
        </slice>
        </transceiver-connectivity>"""

        config = conn.get_config(source=sess, filter=('subtree', template)).data_xml
        pretty_print(config)

    except Exception as e:
        print(e)


def get_step_5(conn, sess):
    try:
        template = """<transceiver-connectivity xmlns="urn:sliceable-transceiver-sdm-connectivity">
        <slice>
        <sliceid>1</sliceid>                
        <optical-signal><opticalchannelid>7</opticalchannelid><monitor><osnr></osnr><ber></ber></monitor></optical-signal>
        <optical-signal><opticalchannelid>8</opticalchannelid><monitor><osnr></osnr><ber></ber></monitor></optical-signal>
        <optical-signal><opticalchannelid>9</opticalchannelid><monitor><osnr></osnr><ber></ber></monitor></optical-signal>
        </slice>
        </transceiver-connectivity>"""

        config = conn.get_config(source=sess, filter=('subtree', template)).data_xml
        pretty_print(config)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    hostRX = '10.1.7.66'
    port = 830
    login = 'root'
    password = 'netlabN.'
    connectionRX = connection.connect(hostRX, port, login, password)
    session = 'running'
    # STEP 1
    get_step_1(connectionRX, session)
    # STEP 2
    get_step_2(connectionRX, session)
    # STEP 3
    get_step_3(connectionRX, session)
    # STEP 4
    get_step_4(connectionRX, session)
    # STEP 5
    get_step_5(connectionRX, session)
    connection.close(connectionRX)
