"""
This module implements ...

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""
from ncclient import manager as m

host = "10.1.7.81"
n = m.connect(host=host, port=830, username='root',
                    password='netlabN.', device_params={'name': 'csr'})  # device handler csr -> Cisco CSR

for capability in n.server_capabilities:
    print(capability)

# yang_model = "toaster"
# schema = n.get_schema(yang_model)
# print(schema.data)

# c = n.get_config(source='running').data_xml
# with open("%s.xml" % host, 'w') as file:
#     file.write(c)

rpc = """
    <get-config>
    <source>
        <running/>
    </source>
    <filter xmlns="urn:opendaylight:params:xml:ns:yang:hello">
        <hello/>
    </filter>
    </get-config>"""

data = n.rpc(rpc)
print(data)

n.close_session()
