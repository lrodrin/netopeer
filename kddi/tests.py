"""
This module implements execution tests

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""

import time

import kddi.sliceable_transceiver_sdm_edit_all as edit
import kddi.sliceable_transceiver_sdm_get as get
import kddi.sliceable_transceiver_sdm_startup as startup

host = '10.1.7.65'
host2 = '10.1.7.66'
port = 830
login = 'root'
password = 'netlabN.'
filter = "<transceiver/>"

# INIT
print("INIT CONNECTIONS")
connectionTX = startup.init_connection(host, port, login, password)
connectionRX = startup.init_connection(host2, port, login, password)

# TEST 1
config_file = 'test1_edit_config.xml'
print("TEST 1\nConfiguration of one spectral and spatial superchannel")
print("create_configuration on %s" % host)
startup.create_configuration(connectionTX, config_file, 'running', 'merge', filter)
print("create_configuration on %s" % host2)
startup.create_configuration(connectionRX, config_file, 'running', 'merge', filter)
print("END TEST 1")

# TEST 2
print("TEST 2\nMeasurement of the OSNR and BER")
get.get_ber_and_osnr_parameters(connectionRX)
print("END TEST 2")

# Sleeping
time.sleep(30)

# TEST 4
print("TEST 4\nMeasurement of the OSNR and BER after the soft failure in the reference core")
get.get_ber_and_osnr_parameters(connectionRX)
print("END TEST 4")

# TEST 5
print("TEST 5\nReconfiguration of the optical channels")
config_file = 'test5_edit_config.xml'
print("set_parameters on %s" % host)
edit.set_parameters(connectionTX, config_file, 'running', 'merge', filter)
print("set_parameters on %s" % host2)
edit.set_parameters(connectionRX, config_file, 'running', 'merge', filter)
print("END TEST 5")

# TEST 6
print("TEST 6\nMeasurement of the OSNR and BER to ensure optical restoration")
get.get_ber_and_osnr_parameters(connectionRX)
print("END TEST 6")

# END
startup.close_connection(connectionTX)
startup.close_connection(connectionRX)
print("CLOSE CONNECTIONS")
