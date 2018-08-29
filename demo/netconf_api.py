#!/usr/bin/python
# -*- coding: utf-8 -*-
import inspect
import logging
import os
import sys
import traceback

from ncclient import manager

__author__ = "Laura Rodriguez <laura.rodriguez@cttc.cat>"
__copyright__ = "Copyright 2018, CTTC"
__license__ = "MIT License"

logger = logging.getLogger('.'.join(os.path.abspath(__name__).split('/')[1:]))


class NETCONF_api:

    def __init__(
            self,
            user,
            password,
            ip,
            port,
    ):
        self.user = user
        self.password = password
        self.ip = ip
        self.port = port

    def addConnnection(self, connectionid, port_in_id, port_out_out, transceiverid):
        # Add connection data to NETCONF server

        logger.debug(format(inspect.stack()[1]))
        logging.debug('netconfApi.insertConnnection')

        data = '''
        <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <node xmlns="urn:node-connectivity">
                <node-id>''' + self.ip + '''</node-id>
                <connection>
                    <connectionid>''' + connectionid + '''</connectionid>
                    <port-in_id>''' + port_in_id + '''</port-in_id>
                    <port-out_out>''' + port_out_out + '''</port-out_out>
                    <transceiver>
                        <transceiverid>''' + transceiverid + '''</transceiverid>
                    </transceiver>
                </connection>
            </node>
        </config>
        '''
        try:
            connection = manager.connect(host='10.0.2.15', port=self.port, username=self.user,
                                         password=self.password, hostkey_verify=False,
                                         device_params={'name': 'default'}, allow_agent=False,
                                         look_for_keys=False)

            connection.edit_config(target='running', config=data, default_operation='merge')

        except Exception as e:
            logger.error({'ERROR': str(sys.exc_info()[0]), 'VALUE': str(sys.exc_info()[1]),
                          'TRACEBACK': str(traceback.format_exc()), 'CODE': 500})
            raise e

    def deleteConnection(self, connectionid):
        # Delete connection data in NETCONF server

        logger.debug(format(inspect.stack()[1]))
        logging.debug('netconfApi.deleteConnection')

        data = '''
        <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <node xmlns="urn:node-connectivity">
                <node-id>''' + self.ip + '''</node-id>
                <connection xmlns="urn:node-connectivity">
                        <connectionid>''' + connectionid + '''</connectionid>
                </connection>
            </node>
        </config>
        '''
        try:
            connection = manager.connect(host='10.0.2.15', port=self.port, username=self.user,
                                         password=self.password, hostkey_verify=False,
                                         device_params={'name': 'default'}, allow_agent=False,
                                         look_for_keys=False)

            connection.edit_config(target='running', config=data, default_operation='replace')

        except Exception as e:
            logger.error({'ERROR': str(sys.exc_info()[0]), 'VALUE': str(sys.exc_info()[1]),
                          'TRACEBACK': str(traceback.format_exc()), 'CODE': 500})
            raise e


if __name__ == '__main__':
    api = NETCONF_api('root', 'netlabN.', '10.1.7.84', 831)
    response = api.addConnnection('05001', '131072', '65536', '1')
    response = api.deleteConnection('05001')
