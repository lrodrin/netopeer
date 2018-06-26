"""
This module implements execution test 4

Copyright (c) 2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""

import time

import jocn.delete as delete
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

# TEST 4
print("TEST 4\nRemoval of all slices")
delete.delete_configuration(connectionTX, 'running')

# Sleeping
time.sleep(30)

delete.delete_configuration(connectionRX, 'running')
print("END TEST 4")

# END
startup.close_connection(connectionTX)
startup.close_connection(connectionRX)
print("CLOSE SERVER CONNECTIONS")
