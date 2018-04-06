#!/usr/bin/env python

__author__ = "Laura Rodriguez <laura.rodriguez@cttc.cat>"
__copyright__ = "Copyright 2018, CTTC"
__license__ = "Apache 2.0"

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This sample application demonstrates use of Python programming language bindings for sysrepo library.
# Original c application was rewritten in Python to show similarities and differences
# between the two.
#
# Most notable difference is in the very different nature of languages, c is weakly statically typed language
# while Python is strongly dynamiclally typed. Python code is much easier to read and logic easier to comprehend
# for smaller scripts. Memory safety is not an issue but lower performance can be expected.
#
# The original c implementation is also available in the source, so one can refer to it to evaluate trade-offs.

import sys

import libsysrepoPython2 as sr
import six


def data_provider_cb():
    six.print_("\n\n ========== HELLO: ==========\n\n")


# Notable difference between c implementation is using exception mechanism for open handling unexpected events.
# Here it is useful because `Connenction`, `Session` and `Subscribe` could throw an exception.
try:
    if len(sys.argv) < 2:
        six.print_("Usage: python application_get.py [module-name]")

    else:
        module_name = sys.argv[1]

        six.print_("Application will watch in " + module_name + "\n")

        # connect to sysrepo
        conn = sr.Connection("example_application")

        # start session
        sess = sr.Session(conn)

        # subscribe for providing operational data
        subs = sr.Subscribe(sess)
        subs.dp_get_items_subscribe("/ietf-interfaces:interfaces-state", data_provider_cb, None,
                                    sr.SR_SUBSCR_DEFAULT | sr.SR_SUBSCR_APPLY_ONLY)

        six.print_("This application will be a data provider for state data of " + module_name + ".\n")
        six.print_("\n\n ========== SUBSCRIBED FOR PROVIDING OPER DATA ==========\n\n")

        sr.global_loop()

        six.print_("Application exit requested, exiting.\n")

except Exception as e:
    six.print_(e)
