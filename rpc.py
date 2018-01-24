"""
This module implements ...

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""
from ncclient import manager, transport, capabilities, operations

hello_rpc_reply = """<hello>
    <capabilities>
        <capability>candidate</capability>
        <capability>validate</capability>
    </capabilities>
    <session-id>s001</session-id>
    </hello>
    """

# connection
connection = manager.connect('10.1.7.81', 830, 'root', 'netlabN.')

# session
device_handler = manager.make_device_handler({'name': 'default'})
capabilities = capabilities.Capabilities(device_handler.get_capabilities())
session = transport.Session(capabilities)

c = connection.take_notification(block=True)
print(c)

obj = operations.RPC(session, device_handler, raise_mode=0, timeout=0)
reply = operations.RPCReply(hello_rpc_reply)
node = manager.new_ele("commit")

# event = operations.RPC(session, device_handler, async=False, timeout=30, raise_mode=0).event.set()
# print(event)
#
# request = operations.RPC(session, device_handler, async=False, timeout=30, raise_mode=0).request()
# print(request)

# session._server_capabilities = [':running']
# rpc = operations.RPC(session, device_handler, raise_mode=operations.RaiseMode.ALL, timeout=0)
# print(rpc)
#
# rpc2 = operations.GetConfig(session, device_handler, async=False, timeout=30, raise_mode=0)
# rpc2.request(source='running', filter=None)

listener = transport.SessionListener()
session.add_listener(listener)


def test_send_connected():
    cap = [':candidate']
    rpc = transport.Session(cap)
    rpc._connected = True
    rpc.send("Hello World")


if __name__ == '__main__':
    test_send_connected()
