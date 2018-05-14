#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import inspect
import json
import logging
import os

from TopologyManager.plugins.NETCONF_plugin.netconf_api import NETCONF_API
from lib.COP.objects_service_topology.topology import Topology
from lib.COP.objects_service_topology.node import Node
from lib.COP.objects_service_topology.edgeEnd import EdgeEnd

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
        self.controller = kwargs['controller']

    def __str__(self):
        return self.name

    def createTopology(self):
        logger.debug(format(inspect.stack()[1]))
        logging.debug('netconfPlugin.createTopology')

        # Topology Manager network representation
        topology = Topology()
        topology_parsed = self.parseTopology(topology)
        return topology_parsed

    def parseTopology(self, topology):
        logger.debug(format(inspect.stack()[1]))
        logging.debug('netconfPlugin.parseTopology')

        topology_retrieved = self.api.retrieveConfiguration()
        topology_json = json.loads(topology_retrieved)
        logger.debug('Topology: {}'.format(json.dumps(topology_json['data']['node'])))

        configNode = topology_json['data']['node']  # node
        node = Node()
        node.nodeId = configNode['node-id']  # node-id
        for netconf_port in configNode['port']:
            port = EdgeEnd()
            port.edgeEndId = netconf_port['port-id']
            port.name = netconf_port['layer-protocol-name']
            node.edgeEnd[port.edgeEndId] = port

        node.nodetype = 'SDM'
        node.domain = str(self.controller.domainId)
        topology.nodes[node.nodeId] = node
        return topology

    def refreshTopology(self, topology):
        logger.debug(format(inspect.stack()[1]))
        logging.debug('netconfPlugin.refreshTopology')

        topology_parsed = self.parseTopology(topology)
        return topology_parsed