"""
This module implements ...

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""

import kddi.data as d


def get_interface_state(host, port, login, password):
    connection = d.connect(host, port, login, password)
    d.get_config(connection, "<interfaces-state/>", 'running')


if __name__ == '__main__':
    host = '10.1.7.67'
    port = 830
    login = 'root'
    password = 'netlabN.'
    config_file = 'test1_edit_config.xml'
    # config_file = 'test5_edit_config.xml'
    filter = "<transceiver/>"

    get_interface_state(host, port, login, password)
