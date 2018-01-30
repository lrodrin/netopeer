"""
This module implements change the node configuration

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""

import data as t

if __name__ == '__main__':
    host = '10.1.7.81'
    port = 830
    connection = t.connect(host, port, 'root', 'netlabN.')  # connection to NETCONF server

    filter = '''<sdm-node xmlns="urn:cttc:params:xml:ns:yang:sdm-node">'''

    # datastore sessions
    session1 = 'startup'
    session2 = 'running'
    session3 = 'candidate'

    # operations
    operation1 = 'merge'
    operation2 = 'replace'

    try:
        filename = open('signal_config.xml')  # open configuration file
        t.edit_config(connection, filename.read(), session2, operation2)  # edit configuration
        print("node configuration edited\nnew configuration:")
        t.get_config(connection, filter, session2)  # get node configuration

    except Exception as e:
        print(e)

    finally:
        connection.close_session()
