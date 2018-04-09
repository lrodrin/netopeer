"""
This module implements execution tests

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""

import time

import kddi.sliceable_transceiver_sdm_edit as edit
import kddi.sliceable_transceiver_sdm_get as get
import kddi.sliceable_transceiver_sdm_startup as startup

host = '10.1.7.67'
host2 = '10.1.7.83'
port = 830
login = 'root'
password = 'netlabN.'
filter = "<transceiver/>"

# INIT
connectionTX = startup.init_connection(host, port, login, password)
connectionRX = startup.init_connection(host2, port, login, password)

# TEST 1
config_file = 'test1_edit_config.xml'
print("TEST 1\nConfiguration of one spectral and spatial superchannel")
startup.create_configuration(connectionTX, config_file, 'running', 'merge', filter)
startup.create_configuration(connectionRX, config_file, 'running', 'merge', filter)

# TEST 2
print("TEST 2\nMeasurement of the OSNR and BER")
get.get_ber_and_osnr_parameters(connectionRX)

# Sleeping
time.sleep(30)

# TEST 4
print("TEST 4\nMeasurement of the OSNR and BER after the soft failure in the reference core")
get.get_ber_and_osnr_parameters(connectionRX)

# TEST 5
print("TEST 5\nReconfiguration of the optical channels")
config_file = 'test5_edit_config.xml'
edit.set_parameters(connectionTX, config_file, 'running', 'merge', filter)
edit.set_parameters(connectionRX, config_file, 'running', 'merge', filter)

# TEST 6
print("TEST 6\nMeasurement of the OSNR and BER to ensure optical restoration")
get.get_ber_and_osnr_parameters(connectionRX)

# END
startup.close_connection(connectionTX)
startup.close_connection(connectionRX)
