"""
This module implements execution tests

Copyright (c) 2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""
# import ofc.sliceable_transceiver_sdm_get as get
import ofc.sliceable_transceiver_sdm_connection as connection
import ofc.sliceable_transceiver_sdm_edit as edit

# hostTX = '10.1.7.65'
hostRX = '10.1.7.66'
port = 830
login = 'root'
password = 'netlabN.'
# filter = "<transceiver-connectivity/>"

# CONNECT
print("INIT CONNECTIONS")
# connectionTX = connection.connect(hostTX, port, login, password)
connectionRX = connection.connect(hostRX, port, login, password)

# STEP 1
config_file = "edit_1.xml"
print("STEP 1\nProvisioning of a slice")
print("Provisioning of one super-channel for a bandwidth request of 216 Gb/s:")
edit.edit_config(connectionRX, config_file, 'running', 'merge')
print("Measurement of the OSNR and BER of all optical sub-channels")
print("END STEP 1")

# TEST 2
config_file = "edit_2.xml"
print("STEP 1\nIncrease of bandwidth by adding modes")
print("Reconfiguration of the super-channel of slice1 to increase the bandwidth to 288 GB/s:")
edit.edit_config(connectionRX, config_file, 'running', 'merge')
print("Measurement of the OSNR and BER of all optical sub-channels")
print("END STEP 2")

# TEST 3
config_file = "edit_3.xml"
print("STEP 1\nIncrease of bandwidth by adding frequency slots")
print("Reconfiguration of the super-channel (slice1) to increase the bandwidth to 576 GB/s:")
edit.edit_config(connectionRX, config_file, 'running', 'merge')
print("Measurement of the OSNR and BER of all optical sub-channels")
print("END STEP 3")

# TEST 4
config_file = "edit_4.xml"
print("STEP 1\nReduction of bandwidth by removing modes ")
print("Reconfiguration of the super-channel to reduce the bandwidth to 432 GB/s:")
edit.edit_config(connectionRX, config_file, 'running', 'replace')
print("Measurement of the OSNR and BER of all optical sub-channels")
print("END STEP 4")

# TEST 5
config_file = "edit_5.xml"
print("STEP 1\nReduction of bandwidth by removing frequency slots")
print("Reconfiguration of the super-channel to reduce the bandwidth to 216 GB/s:")
edit.edit_config(connectionRX, config_file, 'running', 'replace')
print("Measurement of the OSNR and BER of all optical sub-channels")
print("END STEP 5")

# CLOSE
print("CLOSE CONNECTIONS")
# connection.close(connectionTX)
connection.close(connectionRX)
