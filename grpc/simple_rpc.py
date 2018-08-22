#!/usr/bin/env python

from __future__ import print_function, unicode_literals

import json
import os
import pprint

from pyangbind.lib.pybindJSON import dumps
from pyangbind.lib.serialise import pybindJSONDecoder
from rbindings.node_topology_rpc.test.input import input
from rbindings.node_topology_rpc.test.output import output

__author__ = "Laura Rodriguez Navas <laura.rodriguez@cttc.cat>"
__copyright__ = "Copyright 2018, CTTC"

pp = pprint.PrettyPrinter(indent=4)

# Create an input instance
rpc_input = input()
rpc_input.input_container.argument_one = "test_call"
rpc_input.input_container.argument_two = 42
print(dumps(rpc_input, mode="ietf"))

# Load an output from IETF JSON
rpc_output = output()
fn = os.path.join("json", "rpc-output.json")
json_obj = json.load(open(fn, "r"))
pybindJSONDecoder.load_ietf_json(json_obj, None, None, obj=rpc_output)
print(rpc_output.response_id)

pp.pprint(rpc_output.get(filter=True))
