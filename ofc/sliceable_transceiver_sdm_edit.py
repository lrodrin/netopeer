"""
This module implements the edit_config steps for ofc

Copyright (c) 2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""
import xml.dom.minidom as md

import ofc.sliceable_transceiver_sdm_connection as connection

INDENT = ' ' * 4


def pretty_print(s):
    return '\n'.join(line for line in md.parseString(s).toprettyxml(indent=INDENT).split('\n') if line.strip())


def edit_config(conn, config_file, sess, op):
    try:
        f = open(config_file)
        conn.edit_config(target=sess, config=f.read(), default_operation=op)
        f.close()

    except Exception as e:
        print(e)


if __name__ == '__main__':
    hostRX = '10.1.7.66'
    port = 830
    login = 'root'
    password = 'netlabN.'
    config_files = ["edit_1.xml", "edit_2.xml", "edit_3.xml", "edit_4.xml", "edit_5.xml"]
    session = 'running'
    operation = ["merge", "replace"]
    connectionRX = connection.connect(hostRX, port, login, password)
    # STEP 1
    edit_config(connectionRX, config_files[0], session, operation[0])
    # STEP 2
    edit_config(connectionRX, config_files[1], session, operation[0])
    # STEP 3
    edit_config(connectionRX, config_files[2], session, operation[0])
    # STEP 4
    edit_config(connectionRX, config_files[3], session, operation[1])
    # STEP 5
    edit_config(connectionRX, config_files[4], session, operation[1])
    connection.close(connectionRX)
