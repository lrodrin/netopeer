"""
This module implements execution tests

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""

import subprocess

subprocess.call("python sliceable_transceiver_sdm_startup.py", shell=True)  # test1
subprocess.call("python sliceable_transceiver_sdm_get.py", shell=True)  # test2
subprocess.call("python sliceable_transceiver_sdm_get.py", shell=True)  # test4
subprocess.call("python sliceable_transceiver_sdm_edit5.py", shell=True)  # test5
subprocess.call("python sliceable_transceiver_sdm_get.py", shell=True)  # test6
