"""
This module implements the steps for ofc

Copyright (c) 2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""
import xml.dom.minidom as md

import ofc.sliceable_transceiver_sdm_connection as connection

INDENT = ' ' * 4


def pretty_print(s):
    return '\n'.join(line for line in md.parseString(s).toprettyxml(indent=INDENT).split('\n') if line.strip())


def edit_config(conn, config_file, session, operation):
    try:
        f = open(config_file)
        conn.edit_config(target=session, config=f.read(), default_operation=operation)
        f.close()

    except Exception as e:
        print(e)


if __name__ == '__main__':
    hostTX = '10.1.7.65'
    hostRX = '10.1.7.66'
    port = 830
    login = 'root'
    password = 'netlabN.'
    config_files = ["edit_1.xml", "edit_2.xml", "edit_3.xml", "edit_4.xml", "edit_5.xml"]

    connectionRX = connection.connect(hostRX, port, login, password)
    # STEP 1
    edit_config(connectionRX, config_files[0], 'running', 'merge')
    # STEP 2
    edit_config(connectionRX, config_files[1], 'running', 'merge')
    # STEP 3
    edit_config(connectionRX, config_files[2], 'running', 'merge')
    # STEP 4
    edit_config(connectionRX, config_files[3], 'running', 'replace')
    # STEP 5
    edit_config(connectionRX, config_files[4], 'running', 'replace')

    connection.close(connectionRX)
