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

# Notable difference between c implementation is using exception mechanism for open handling unexpected events.
# Here it is useful because `Conenction`, `Session` and `Subscribe` could throw an exception.
try:
    if len(sys.argv) < 2:
        six.print_("Usage: python application_get.py [module-name]")

    else:
        module_name = sys.argv[1]

        six.print_("Application will watch for gets in " + module_name + "\n")

        # connect to sysrepo
        # conn = sr.Connection("example_application")
        conn = sr.Connection("app2")

        # start session
        sess = sr.Session(conn)

        select_xpath = "/" + module_name + ":*//*"

        values = sess.get_items(select_xpath)

        for i in range(values.val_cnt()):
            six.print_(values.val(i).to_string())

except Exception as e:
    six.print_(e)
