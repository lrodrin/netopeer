"""
This module implements ...

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""
from ncclient import manager

n = manager.connect(host='10.1.7.81', port=830, username='root',
                    password='netlabN.', device_params={'name': 'csr'})

schema = n.get_schema('toaster')
print(schema)