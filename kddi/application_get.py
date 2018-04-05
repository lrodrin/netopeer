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


# Helper function for printing changes given operation, old and new value.
def print_change(op, old_val, new_val):
    if op == sr.SR_OP_CREATED:
        six.print_("CREATED: ", end=" ")
        six.print_(new_val.to_string())
    elif op == sr.SR_OP_DELETED:
        six.print_("DELETED: ", end=" ")
        six.print_(old_val.to_string())
    elif op == sr.SR_OP_MODIFIED:
        six.print_("MODIFIED: ")
        six.print_("old value", end=" ")
        six.print_(old_val.to_string())
        six.print_("new value", end=" ")
        six.print_(new_val.to_string())
    elif op == sr.SR_OP_MOVED:
        six.print_("MOVED: " + new_val.xpath() + " after " + old_val.xpath())


# Helper function for printing events.
def ev_to_str(ev):
    if ev == sr.SR_EV_VERIFY:
        return "verify"
    elif ev == sr.SR_EV_APPLY:
        return "apply"
    elif ev == sr.SR_EV_ABORT:
        return "abort"
    else:
        return "abort"


# Function to print current configuration state.
# It does so by loading all the items of a session and printing them out.
def data_requester(session, module):
    select_xpath = "/" + module + ":transceiver/slice[sliceid='1']/optical-signal/monitor//*"

    values = session.get_items(select_xpath)

    if values is not None:
        for i in range(0, 24):
            six.print_(values.val(i).to_string())


# Function to be called for subscribed client of given session whenever configuration changes.
def module_change_cb(session, module, event, private_ctx):
    try:
        six.print_(
            "\n\n ========== Notification " + ev_to_str(event) + " =============================================\n")
        if sr.SR_EV_APPLY == event:
            six.print_("\n ========== CONFIG HAS CHANGED, CURRENT RUNNING CONFIG: ==========\n")
            data_requester(session, module)

        six.print_("\n ========== CHANGES: =============================================\n")

        change_path = "/" + module + ":*"

        it = session.get_changes_iter(change_path)

        while True:
            change = session.get_change_next(it)
            if change is None:
                break
            print_change(change.oper(), change.old_val(), change.new_val())

        six.print_("\n\n ========== END OF CHANGES =======================================\n")

    except Exception as error:
        six.print_(error)

    return sr.SR_ERR_OK


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

        # subscribe for changes in running config
        # subscribe = sr.Subscribe(sess)
        # subscribe.module_change_subscribe(module_name, module_change_cb, None, 0,
        #                                   sr.SR_SUBSCR_DEFAULT | sr.SR_SUBSCR_APPLY_ONLY)
        try:
            data_requester(sess, module_name)

        except Exception as e:
            six.print_(e)

        # six.print_("\n\n ========== STARTUP CONFIG APPLIED AS RUNNING ==========\n")
        #
        # sr.global_loop()
        #
        # six.print_("Application exit requested, exiting.\n")

except Exception as e:
    six.print_(e)