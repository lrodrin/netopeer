"""
This module implements execution test 1

Copyright (c) 2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""

import time

import jocn.get_state as get
import jocn.startup as startup

hostTX = '10.1.7.65'
hostRX = '10.1.7.66'
port = 830
login = 'root'
password = 'netlabN.'
filter = "<transceiver-connectivity/>"

# INIT
print("INIT SERVER CONNECTIONS")
connectionTX = startup.init_connection(hostTX, port, login, password)
connectionRX = startup.init_connection(hostRX, port, login, password)

# TEST 1
test1_config_file = 'test1.xml'
print("TEST 1\nConfiguration of slice 1")
print("create_configuration on %s" % hostTX)
startup.create_configuration(connectionTX, test1_config_file, 'running', 'merge', filter)
print("create_configuration on %s" % hostRX)
startup.create_configuration(connectionRX, test1_config_file, 'running', 'merge', filter)

# Sleeping
time.sleep(30)

print("TEST 1\nMeasurement of the OSNR and BER")
get.get_ber_and_osnr_parameters(connectionRX)
print("END TEST 1")

# END
startup.close_connection(connectionTX)
startup.close_connection(connectionRX)
print("CLOSE SERVER CONNECTIONS")
