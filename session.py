"""
This module implements ...

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""
from ncclient import manager, transport, capabilities

# connection
connection = manager.connect('10.1.7.81', 830, 'root', 'netlabN.')

# session
device_handler = manager.make_device_handler({'name': 'default'})
capabilities = capabilities.Capabilities(device_handler.get_capabilities())
session = transport.Session(capabilities)

# session._server_capabilities = [':running']
# rpc = operations.RPC(session, device_handler, raise_mode=operations.RaiseMode.ALL, timeout=0)
# print(rpc)
#
# rpc2 = operations.GetConfig(session, device_handler, async=False, timeout=30, raise_mode=0)
# rpc2.request(source='running', filter=None)
