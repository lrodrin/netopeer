"""
This module implements some code about the class ncclient, a NETCONF Python client

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""
from ncclient import manager


def connect(host):
    m = manager.connect(host=host, port=830, username='root', password='netlabN.', hostkey_verify=False,
                        device_params={'name': 'csr'})  # device handler csr -> Cisco CSR
    return m


def get_capabilities(m):
    for c in m.server_capabilities:  # display the NETCONF server capabilities
        print(c)


def get_yang_schema(m, yang_model):  # obtain a YANG model specified by yang_model
    schema = m.get_schema(yang_model)
    print(schema.data)


# def edit_config(m):
#     # retrieve the running config from the NETCONF server using get-config and write the XML config to file
#     c = m.get_config(source='running').data_xml
#     with open("get_config.xml", 'w') as file:
#         file.write(c)


def get_config(m):
    # retrieve the running config from the NETCONF server using get-config and write the XML config to file
    c = m.get_config(source='running').data_xml
    f = open("get_config.xml", "w")
    f.write(c)
    f.close()


if __name__ == '__main__':
    h = '10.1.7.81'
    n = connect(h)
    try:
        get_capabilities(n)
        get_yang_schema(n, 'hello')
        get_config(n)
        # edit_config(n)
    finally:
        n.close_session()
