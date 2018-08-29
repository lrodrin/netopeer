#!/usr/bin/python
# -*- coding: utf-8 -*-
import traceback
import logging
import os
import sys
import time
import copy

from common.config import ConfigObject
from ProvisioningManager.NETCONF_plugin.netconf_api import NETCONF_api
from lib.ABNO_objects.response import Response
from lib.COP.objects_common.error import Error
from common.abno_cop_client import API
from threading import Lock

if sys.version_info >= (3, 0):
    import configparser as ConfigParser
    import queue as Queue
else:
    import ConfigParser
    import Queue

sys.path.append('/'.join([element for i, element in
                          enumerate(os.path.abspath(__file__).split('/'))
                          if i < len(os.path.abspath(__file__).split('/')) - 3]))

__author__ = "Laura Rodriguez <laura.rodriguez@cttc.cat>"
__copyright__ = "Copyright 2018, CTTC"
__license__ = "MIT License"

logger = logging.getLogger('.'.join(os.path.abspath(__name__).split('/')[1:]))

config = ConfigObject().config_storage['provisioning_service_settings']


class NETCONF_plugin:

    def __init__(self, **kwargs):
        for key in ('ctl_addr', 'ctl_port', 'ctl_user', 'ctl_password', 'ctl_nthreads', 'ctl_operativemode','ctl_flowmeters'):
            if key in kwargs:
                setattr(self, key.split('_')[1], kwargs[key])

        # API Initialization
        self.api = NETCONF_api(self.user, self.password, self.addr,
                           self.port)
        self.name = 'NETCONF'
 

    def create_connection(self, connection):            
        logger.info("Sending new connection to create in NETCONF: " + str(connection))
        self.api.addConnnection(connection.connectionId, connection.aEnd.edgeEndId, connection.zEnd.edgeEndId, '1') 
        response = Response({'message':'Successful create connection operation','result':'successful',
                                    'content':{'connection':connection.json_serializer(),
                                               'success_responses':["OK"]}})       
        return response


    def update_connection(self, **kwargs):
        pass

    def remove_connection(self, connection, id=None):     
        if id:
            connectionId = id
        else:
            connectionId = connection.connectionId

        logger.info("Sending new connection to remove in NETCONF: " + str(connection))
        self.api.deleteConnection(connectionId)
        response = Response({'message':'Successful delete connection operation','result':'successful',
                                        'content':{'connection':connection.json_serializer(),
                                                   'success_responses':["OK"]}})  
        return response                                   

    def remove_all_connections(self, **kwargs):
        logger.info("Removing old connections")
        return Response({'message':'Successful remove all connections operation','result':'successful',
                         'content':{}})

    def clear(self):
        logger.info("Clear")
        
