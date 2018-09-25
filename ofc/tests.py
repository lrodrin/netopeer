"""
This module implements execution tests

Copyright (c) 2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""
import ofc.sliceable_transceiver_sdm_connection as c
import ofc.sliceable_transceiver_sdm_edit as e
import ofc.sliceable_transceiver_sdm_get as g

hostTX = '10.1.7.65'
hostRX = '10.1.7.66'
port = 830
login = 'root'
password = 'netlabN.'
session = 'running'
operation = ["merge", "replace"]

# CONNECT
print("INIT SESSIONS")
connectionTX = c.connect(hostTX, port, login, password)
connectionRX = c.connect(hostRX, port, login, password)

# STEP 1
config_file = "edit_1.xml"
print("STEP 1\nProvisioning of a slice")
print("Provisioning of one super-channel for a bandwidth request of 216 Gb/s:")
e.edit_config(connectionTX, config_file, session, operation[0])
e.edit_config(connectionRX, config_file, session, operation[0])
print("Measurement of the OSNR and BER of all optical sub-channels")
g.get_step_1(connectionRX, session)
print("END STEP 1")
# sleep(30)

# TEST 2
config_file = "edit_2.xml"
print("STEP 2\nIncrease of bandwidth by adding modes")
print("Reconfiguration of the super-channel of slice1 to increase the bandwidth to 288 GB/s:")
e.edit_config(connectionTX, config_file, session, operation[0])
e.edit_config(connectionRX, config_file, session, operation[0])
print("Measurement of the OSNR and BER of all optical sub-channels")
g.get_step_2(connectionRX, session)
print("END STEP 2")
# sleep(30)

# TEST 3
config_file = "edit_3.xml"
print("STEP 3\nIncrease of bandwidth by adding frequency slots")
print("Reconfiguration of the super-channel (slice1) to increase the bandwidth to 576 GB/s:")
e.edit_config(connectionTX, config_file, session, operation[0])
e.edit_config(connectionRX, config_file, session, operation[0])
print("Measurement of the OSNR and BER of all optical sub-channels")
g.get_step_3(connectionRX, session)
print("END STEP 3")
# sleep(30)

# TEST 4
config_file = "edit_4.xml"
print("STEP 4\nReduction of bandwidth by removing modes ")
print("Reconfiguration of the super-channel to reduce the bandwidth to 432 GB/s:")
e.edit_config(connectionTX, config_file, session, operation[1])
e.edit_config(connectionRX, config_file, session, operation[1])
print("Measurement of the OSNR and BER of all optical sub-channels")
g.get_step_4(connectionRX, session)
print("END STEP 4")
# sleep(30)

# TEST 5
config_file = "edit_5.xml"
print("STEP 5\nReduction of bandwidth by removing frequency slots")
print("Reconfiguration of the super-channel to reduce the bandwidth to 216 GB/s:")
e.edit_config(connectionTX, config_file, session, operation[1])
e.edit_config(connectionRX, config_file, session, operation[1])
print("Measurement of the OSNR and BER of all optical sub-channels")
g.get_step_5(connectionRX, session)
print("END STEP 5")

# CLOSE
print("CLOSE SESSIONS")
c.close(connectionTX)
c.close(connectionRX)
