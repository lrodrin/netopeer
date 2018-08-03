"""
This module implements ...

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""

from ncclient import manager

connection_1 = manager.connect(host='10.1.7.83', port=831, username='root', password='netlabN.', hostkey_verify=False,
                               device_params={'name': 'default'}, allow_agent=False, look_for_keys=False)
print('connection: ', connection_1.connected)

connection_2 = manager.connect(host='10.1.7.83', port=832, username='root', password='netlabN.', hostkey_verify=False,
                               device_params={'name': 'default'}, allow_agent=False, look_for_keys=False)
print('connection: ', connection_2.connected)

connection_3 = manager.connect(host='10.1.7.83', port=833, username='root', password='netlabN.', hostkey_verify=False,
                               device_params={'name': 'default'}, allow_agent=False, look_for_keys=False)
print('connection: ', connection_3.connected)
