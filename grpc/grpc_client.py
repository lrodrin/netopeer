#!/usr/bin/env python

import json
import sys

from pynms_grpc.client.client_common import PyNMSConfigOperation
from pynms_grpc.client.pynms_grpc_client import PyNMSGRPCClient
from pynms_yang_examples.bindings import node_topology


def print_get(msg):
    for res in msg.response:
        print
        "%s\n------\n" % (res.path)
        print
        json.dumps(json.loads(res.value), indent=4)


def main():
    client = PyNMSGRPCClient('localhost', 50051)
    client.run()

    nt = node_topology()

    nt.node.node_id = "10.1.7.65"
    pl = nt.node.port.add("01")
    for core in [("00", "Core0"), ("01", "Core1")]:
        ac = pl.available_core.add(core[0])
        ac.core_id.available_core = core[1]

    transaction = [PyNMSConfigOperation(nt.node, 'UPDATE_CONFIG')]
    msg = client.set_paths(transaction, request_id=41)

    if msg.response_code == 0:
        print
        "Successfully updated /node!"

    print
    "Following set, interfaces content is"
    msg = client.get_paths(["/node"], 42)
    print_get(msg)

    sys.exit(0)


if __name__ == '__main__':
    main()
