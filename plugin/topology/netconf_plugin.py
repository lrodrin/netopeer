#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import inspect
import logging
import os

from TopologyManager.plugins.NETCONF_plugin.netconf_api import NETCONF_API
from lib.COP.objects_service_topology.topology import Topology

__author__ = "Laura Rodriguez <laura.rodriguez@cttc.cat>"
__copyright__ = "Copyright 2018, CTTC"
__license__ = "MIT License"

logger = logging.getLogger('.'.join(os.path.abspath(__name__).split('/')[1:]))


class NETCONF_plugin(object):

    def __init__(self, **kwargs):

        for key in (
                'ctl_name',
                'ctl_addr',
                'ctl_port',
                'ctl_user',
                'ctl_password'):
            if key in kwargs:
                setattr(self, key[4:], kwargs[key])

        self.api = NETCONF_API(self.user, self.password, self.addr, self.port)
        # self.controller = kwargs['controller']

    def __str__(self):
        return self.name

    def createTopology(self):
        logger.debug(format(inspect.stack()[1]))
        logging.debug('netconfPlugin.createTopology')

        topology = Topology()
        topology_parsed = self.parseTopology(topology)
        return topology_parsed

    def parseTopology(self, topology):
        logger.debug(format(inspect.stack()[1]))
        logging.debug('netconfPlugin.parseTopology')

        topology_json = self.api.retrieveConfiguration()
        topology_tmp = Topology(topology_json)
        topology.topologyId = topology_tmp.topologyId
        return topology

    def refreshTopology(self, topology):
        logger.debug(format(inspect.stack()[1]))
        logging.debug('netconfPlugin.refreshTopology')

        topology_parsed = self.parseTopology(topology)
        return topology_parsed