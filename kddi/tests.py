"""
This module implements execution tests

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""

import time

import sliceable_transceiver_sdm_edit5 as edit5
import sliceable_transceiver_sdm_get as get
import sliceable_transceiver_sdm_startup as startup

host = '10.0.34.108'
host2 = '10.0.34.112'
port = 830
login = 'root'
password = 'root'
filter = "<transceiver/>"

# TEST 1
config_file = 'test1_edit_config.xml'

connectionTX = startup.init_connection(host, port, login, password)
connectionRX = startup.init_connection(host2, port, login, password)
startup.create_configuration(connectionTX, config_file, 'running', 'merge', filter)
startup.create_configuration(connectionRX, config_file, 'running', 'merge', filter)

# TEST 2
get.get_ber_and_osnr_parameters(connectionRX)

# Sleeping
time.sleep(30)

# TEST 4
get.get_ber_and_osnr_parameters(connectionRX)

# TEST 5
config_file = 'test5_edit_config.xml'
edit5.set_parameters(connectionTX, config_file, 'running', 'merge', filter)
edit5.set_parameters(connectionRX, config_file, 'running', 'merge', filter)

# TEST 6
get.get_ber_and_osnr_parameters(connectionRX)

# END
startup.close_connection(connectionTX)
startup.close_connection(connectionRX)
