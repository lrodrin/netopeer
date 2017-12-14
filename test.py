"""
This module implements ...

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""
from ncclient import manager

n = manager.connect(host='10.1.7.81', port=830, username='root',
                    password='netlabN.', device_params={'name': 'csr'})  # device handler csr -> Cisco CSR

# for c in n.server_capabilities:
#     print(c)

yang_model = "toaster"
schema = n.get_schema(yang_model)
print(schema.data)

for capability in n.server_capabilities:
    print(capability)

n.close_session()
