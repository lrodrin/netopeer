"""
This module create the sliceable transceiver sdm configuration

Copyright (c) 2018-2019 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""

import kddi.data as d

# datastore sessions
session_startup = 'startup'
session_running = 'running'
session_candidate = 'candidate'

# NETCONF operations
operation_merge = 'merge'
operation_replace = 'replace'


def change_node_config(host, port, login, password, config_file, session, operation, filter):
    connection = d.connect(host, port, login, password)  # connection to NETCONF server

    snippet = """<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
          <transceiver xmlns="urn:sliceable-transceiver-sdm">
            <slice> <sliceid> <optical-channel>
            <coreid>%s</coreid> <uid>%s</uid> <gid>%s</gid>
            <password>*</password> <ssh_keydir/> <homedir/>
          </optical-channel></sliceid></slice></transceiver></config>""" % ("Core19", uid, gid)

    try:
        print(d.get_config(connection, filter, session))


    except Exception as e:
        print(e)

    finally:
        connection.close_session()


if __name__ == '__main__':
    host = '10.1.7.67'
    port = 830
    login = 'root'
    password = 'netlabN.'
    config_file = 'slice1_add.xml'
    filter = "</coreid>"

    change_node_config(host, port, login, password, config_file, session_running, operation_merge, filter)
