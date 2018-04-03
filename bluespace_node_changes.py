"""
This module implements change the node configuration

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""

import sys

import data as d

# datastore sessions
session_startup = 'startup'
session_running = 'running'
session_candidate = 'candidate'

# NETCONF operations
operation_merge = 'merge'
operation_replace = 'replace'


def change_signal_config(host, port, login, password, nodeid, location, componentid, param1, param2, param3, param4,
                         wdmid, portid,
                         signalid, wavelength, mode, core):
    connection = d.connect(host, port, login, password)  # connection to NETCONF server

    namespace = '''<bluespace-node xmlns="urn:cttc:params:xml:ns:yang:bluespace_node">'''
    component_config = '''
    <?xml version="1.0" encoding="UTF-8"?>
    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <bluespace-node xmlns="urn:cttc:params:xml:ns:yang:bluespace_node">
            <bluespace-node-id>''' + nodeid + '''</bluespace-node-id>
            <location>''' + location + '''</location>
            <components>
                <component-id>''' + componentid + '''</component-id>
                <analog-rof>
                    <param1>''' + param1 + '''</param1>
                </analog-rof>
                <digital-rof>
                    <param2>''' + param2 + '''</param2>
                </digital-rof>
                <optical-beam-forming>
                    <param3>''' + param3 + '''</param3>
                </optical-beam-forming>
                <ethernet>
                    <param4>''' + param4 + '''</param4>
                </ethernet>
                <sdm-wdm>
                    <wdm-id>''' + wdmid + '''</wdm-id>
                    <port>
                        <port-id>''' + portid + '''</port-id>
                        <signal>
                            <signal-id>''' + signalid + '''</signal-id>
                            <wavelength>''' + wavelength + '''</wavelength>
                            <mode>''' + mode + '''</mode>
                            <core>''' + core + '''</core>
                        </signal>
                    </port>
                </sdm-wdm>
            </components>
        </bluespace-node>
    </config>
    '''

    try:
        d.edit_config(connection, component_config, session_running, operation_replace)  # edit configuration
        print("node configuration edited\nnew configuration:")
        d.get_config(connection, namespace, session_running)  # get node configuration

    except Exception as e:
        print(e)

    finally:
        connection.close_session()


if __name__ == '__main__':
    if len(sys.argv) != 14:
        print(
            "Usage: python sliceable_transceiver_sdm_edit5.py [nodeid] [location] [componentid] [param1] [param2] [param3] ["
            "param4] [wdm-id] [port-id] [signal-id] [wavelength] [mode] [core]")
        print("Example: python sliceable_transceiver_sdm_edit5.py a CO 01 01 02 03 04 01 3000 3001 2 03 3")

    else:
        host = '10.1.7.65'
        port = 830
        login = 'root'
        password = 'netlabN.'

        change_signal_config(host, port, login, password, sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4],
                             sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10],
                             sys.argv[11], sys.argv[12], sys.argv[13])
