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

from lib.COP.objects_service_topology.sdmEdge import SdmEdge
from lib.COP.objects_service_topology.sdmCore import SdmCore
from lib.COP.objects_service_topology.transceiver import Transceiver
from lib.COP.objects_service_topology.frequency import Frequency

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

        topology = Topology()
        topology_parsed = self.parseTopology(topology)
        return topology_parsed

    def parseTopology(self, topology):
        logger.debug(format(inspect.stack()[1]))
        logging.debug('netconfPlugin.parseTopology')

        topology_retrieved = self.api.retrieveConfiguration('<node/>')  # retrieve node-topology configuration
        topology_json = json.loads(topology_retrieved)
        logger.debug('Topology: {}'.format(json.dumps(topology_json['data']['node'])))
        topoNode = topology_json['data']['node']  # node

        node = Node()
        node.nodeId = topoNode['node-id']
        node.nodetype = 'SDM'
        node.domain = str(self.controller.domainId)

        ports = topoNode['port']  # list of ports
        for netconf_port in ports:
            port = EdgeEnd()
            port.edgeEndId = netconf_port['port-id']
            port.name = netconf_port['layer-protocol-name']
            node.edgeEnd[port.edgeEndId] = port

            available_cores = netconf_port['available-core']  # list of cores
            available_transceiver = netconf_port['available-transceiver']  # transceiver

            for netconf_core in available_cores:
                core = SdmCore()
                core.coreId = netconf_core['core-id']

                available_frequency = netconf_core[
                    'available-frequency-slot']  # TODO crear un mateixa funció per les dues llistes
                for netconf_frequency in available_frequency:
                    frequencyA = Frequency()
                    frequencyA.slotId = netconf_frequency['slot-id']
                    frequencyA.gridType = netconf_frequency['nominal-central-frequency']['grid-type']
                    frequencyA.adjustGranularity = netconf_frequency['nominal-central-frequency'][
                        'adjustment-granularity']
                    frequencyA.numChannel = netconf_frequency['nominal-central-frequency']['channel-number']
                    frequencyA.numSlotWidth = netconf_frequency['slot-width-number']
                    core.availableFrequency[frequencyA.slotId] = frequencyA

                occupied_frequency = netconf_core['occupied-frequency-slot']
                for netconf_frequency in occupied_frequency:
                    frequencyO = Frequency()
                    frequencyO.slotId = netconf_frequency['slot-id']
                    frequencyO.gridType = netconf_frequency['nominal-central-frequency']['grid-type']
                    frequencyO.adjustGranularity = netconf_frequency['nominal-central-frequency'][
                        'adjustment-granularity']
                    frequencyO.numChannel = netconf_frequency['nominal-central-frequency']['channel-number']
                    frequencyO.numSlotWidth = netconf_frequency['slot-width-number']
                    core.occupiedFrequency[frequencyO.slotId] = frequencyO

                port.availableCore[core.coreId] = core

                transceiver = Transceiver()
                transceiver.transceiverId = available_transceiver['transceiver-id']
                transceiver.transceiverType = available_transceiver['transceiver-type']
                transceiver.modId = available_transceiver['supported-modulation-format']['modulation-id']
                transceiver.modType = available_transceiver['supported-modulation-format']['mod-type']
                transceiver.maxCf = available_transceiver['supported-center-frequency-range']['max-cf']
                transceiver.minCf = available_transceiver['supported-center-frequency-range']['min-cf']
                transceiver.maxBw = available_transceiver['supported-bandwidth']['max-bw']
                transceiver.minBw = available_transceiver['supported-bandwidth']['min-bw']
                transceiver.fec = available_transceiver['supported-FEC']
                transceiver.equalization = available_transceiver['supported-equalization']
                transceiver.monitoring = available_transceiver['supported-monitoring']
                port.availableTransceiver[transceiver.transceiverId] = transceiver

        topology.nodes[node.nodeId] = node

        return topology

    def refreshTopology(self, topology):
        logger.debug(format(inspect.stack()[1]))
        logging.debug('netconfPlugin.refreshTopology')

        topology_parsed = self.parseTopology(topology)
        return topology_parsed