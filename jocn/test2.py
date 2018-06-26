"""
This module implements execution test 2

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

# TEST 2
test2_config_file = 'test2.xml'
print("TEST 2\nConfiguration of slice 2")
print("create_configuration on %s" % hostTX)
startup.create_configuration(connectionTX, test2_config_file, 'running', 'merge', filter)
print("create_configuration on %s" % hostRX)
startup.create_configuration(connectionRX, test2_config_file, 'running', 'merge', filter)

# Sleeping
time.sleep(30)

print("TEST 2\nMeasurement of the OSNR and BER")
get.get_ber_and_osnr_parameters(connectionRX)
print("END TEST 2")

# END
startup.close_connection(connectionTX)
startup.close_connection(connectionRX)
print("CLOSE SERVER CONNECTIONS")
