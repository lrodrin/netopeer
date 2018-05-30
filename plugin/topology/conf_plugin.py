#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import sys
import logging
import inspect

from TopologyManager.plugins.CONF_plugin.conf_api import CONF_API

sys.path.append('../')

from lib.COP.objects_service_topology.ethEdge import EthEdge
from lib.COP.objects_service_topology.node import Node
from lib.COP.objects_service_topology.edgeEnd import EdgeEnd
from lib.COP.objects_service_topology.dwdmEdge import DwdmEdge
from lib.COP.objects_service_topology.dwdmChannel import DwdmChannel
from lib.COP.objects_service_topology.sdmEdge import SdmEdge
from lib.COP.objects_service_topology.bitmap import Bitmap
from lib.COP.objects_common.keyedArrayType import KeyedArrayType
from lib.COP.objects_service_topology.topology import Topology

__author__ = "Ricard Vilalta <ricard.vilalta@cttc.cat> and Laura Rodriguez <laura.rodriguez@cttc.cat>"
__copyright__ = "Copyright 2018, CTTC"
__license__ = "MIT License"

logger = logging.getLogger('.'.join(os.path.abspath(__name__).split('/')[1:]))


class CONF_plugin(object):

    def __init__(self, **kwargs):

        for key in (
                'ctl_name',
                'ctl_addr',
                'ctl_port',
                'ctl_config_file'):
            if key in kwargs:
                setattr(self, key[4:], kwargs[key])

        # CONFIG DATA
        self.api = CONF_API(self.addr, self.port)
        self.controller = kwargs['controller']

    def __str__(self):
        return self.name

    def createTopology(self):
        logger.debug(format(inspect.stack()[1]))
        logging.debug('confPlugin.createTopology')

        topology = Topology()
        topology_parsed = self.parseTopology(topology)
        self.topology = topology_parsed
        return topology_parsed

    def parseTopology(self, topology):
        logger.debug(format(inspect.stack()[1]))
        logging.debug('confPlugin.parseTopology')

        file_ = self.api.openFile(self.config_file)
        topology_parsed = self.parseXMLtopology(topology, file_)
        return topology_parsed

    def parseXMLtopology(self, topology, xmldoc):
        logger.debug(format(inspect.stack()[1]))
        logging.debug('netconfPlugin.parseXMLtopology')

        nodeList = xmldoc.getElementsByTagName('node')
        linkList = xmldoc.getElementsByTagName('link')

        for i in range(len(nodeList)):
            node = Node()
            node.nodeId = str(nodeList[i].getElementsByTagName('id')[0].childNodes[0].nodeValue)
            node.domain = str(self.controller.domainId)
            topology.nodes[node.nodeId] = node

        for i in range(len(linkList)):
            source_node_value = (linkList[i].getElementsByTagName('source')[0]
                                 .childNodes[0].nodeValue
                                 )
            target_node_value = (linkList[i].getElementsByTagName('target')[0]
                                 .childNodes[0].nodeValue
                                 )

            link_id = str(source_node_value) + '_to_' + str(target_node_value)

            number_of_cores = len(linkList[i].getElementsByTagName('sdm_coreid'))

            for node in topology.nodes:
                if topology.nodes[node].nodeId == source_node_value:
                    src_node = topology.nodes[node]
                    src_port = (
                        linkList[i].getElementsByTagName('local_ifid')[0]
                            .childNodes[0].nodeValue
                    )
                elif topology.nodes[node].nodeId == target_node_value:
                    dest_node = topology.nodes[node]
                    dest_port = (
                        linkList[i].getElementsByTagName('remote_ifid')[0]
                            .childNodes[0].nodeValue
                    )
            switching_cap_type = str(linkList[i]
                                     .getElementsByTagName('iscd')[0]
                                     .getElementsByTagName('item')[0]
                                     .getElementsByTagName('switching_cap')[0]
                                     .childNodes[0].nodeValue
                                     )
            channel_count = int(
                linkList[i].getElementsByTagName('channels')[0]
                    .getElementsByTagName('count')[0]
                    .childNodes[0].nodeValue
            )

            if int(switching_cap_type) == 1:
                if channel_count > 0:
                    e = self.create_edge(i, linkList, link_id, 'DWDM')  # DWDM Edge
                else:
                    e = self.create_edge(i, linkList, link_id, 'ETH')  # ETH Edge

                switching_cap = 'psc'
                self.set_edge_parameters(channel_count, dest_node, dest_port, e, i, linkList, src_node, src_port,
                                         switching_cap, topology, False)
                topology.edges[e.edgeId] = e

            elif int(switching_cap_type) == 150:
                switching_cap = 'lsc'
                e = self.create_edge(i, linkList, link_id, 'DWDM')  # DWDM Edge
                self.set_edge_parameters(channel_count, dest_node, dest_port, e, i, linkList, src_node, src_port,
                                         switching_cap, topology, False)
                topology.edges[e.edgeId] = e

            elif int(switching_cap_type) == 160:
                for j in range(0, number_of_cores):
                    switching_cap = 'sdm'
                    e = self.create_edge(i, linkList, link_id, 'SDM')  # SDM Edge
                    self.set_edge_parameters(channel_count, dest_node, dest_port, e, j, linkList, src_node, src_port,
                                             switching_cap, topology, True)
                    topology.edges[e.edgeId] = e

        logger.debug('Composed CONF topology: {}'.format(topology))
        return topology

    def refreshTopology(self, topology):
        logger.debug(format(inspect.stack()[1]))
        logging.debug('confPlugin.refreshTopology')

        if len(self.topology.edges) > 0:
            return self.topology
        else:
            self.parseTopology(topology)
            return topology

    def create_edge(self, i, linkList, link_id, edge_type):
        edge = None
        if edge_type == 'DWDM':
            edge = DwdmEdge()
            edge.edgeType.set(1)
            edge.delay = str(linkList[i].getElementsByTagName('delay')[0]
                             .childNodes[0].nodeValue)

        elif edge_type == 'ETH':
            edge = EthEdge()
            edge.edgeType.set(2)

        elif edge_type == 'SDM':
            edge = SdmEdge()
            edge.edgeType.set(4)
            edge.delay = str(linkList[i].getElementsByTagName('delay')[0]
                             .childNodes[0].nodeValue)

        logger.debug('%s - %s Edge' % (link_id, edge_type))
        return edge

    def set_edge_parameters(self, channel_count, dest_node, dest_port, edge, index, linkList, src_node, src_port,
                            switching_cap, topology, is_sdm_edge):

        edge.source = str(src_node.nodeId)
        edge.localIfid = str(src_port)
        edge.target = str(dest_node.nodeId)
        edge.remoteIfid = str(dest_port)
        edge.metric = str(linkList[index].getElementsByTagName('te_metric')[0]
                          .childNodes[0].nodeValue)

        if is_sdm_edge:
            edge.edgeId = str(edge.source) + '_to_' + str(edge.target) + '_coreId_' + str(index)
            edge.coreId = str(index)

        else:
            edge.edgeId = str(edge.source) + '_to_' + str(edge.target)

        edge.switchingCap = switching_cap

        edgeEndNotFound = False
        try:
            if not topology.nodes[edge.source].edgeEnd[edge.localIfid]:
                pass

        except:
            edgeEndNotFound = True

        if not edgeEndNotFound:  # if topology.nodes[e.source].edgeEnd[e.localIfid] exists then
            port = EdgeEnd()
            port.edgeEndId = edge.localIfid
            port.peerNodeId = topology.nodes[edge.target].nodeId
            port.switchingCap = switching_cap
            topology.nodes[edge.source].edgeEnd[edge.localIfid] = port

        edge.maxResvBw = str(linkList[index].getElementsByTagName('max_resv_bw')[0]
                             .childNodes[0].nodeValue)
        edge.unreservBw = str(linkList[index].getElementsByTagName('unresv_bw')[0]
                              .getElementsByTagName('item')[0].childNodes[0].nodeValue)

        channelsOcupied = []
        if edge.edgeType.get() == 1:
            logger.debug('Edge: %s', str(edge))
            edge.channels = KeyedArrayType(DwdmChannel, 'g694Id')
            for item in linkList[index].getElementsByTagName('channels')[0].getElementsByTagName('item'):
                channel = DwdmChannel()
                channel.g694Id = int(item.getElementsByTagName('g694_id')[0].childNodes[0].nodeValue)
                channel.state = int(item.getElementsByTagName('state')[0].childNodes[0].nodeValue)
                if channel.state == 2:
                    logger.debug(self.__get_channel(channel.g694Id))
                    channelsOcupied.append(self.__get_channel(channel.g694Id))

                edge.channels[item.getElementsByTagName('g694_id'
                                                        )[0].childNodes[0].nodeValue] = channel

            edge.bitmap = Bitmap(
                {
                    'numChannels': channel_count,
                    'arrayBits': [0] * channel_count
                }
            )
            for index in range(len(channelsOcupied)):
                edge.bitmap.setChannel(channelsOcupied[index])

    @staticmethod
    def __get_channel(label):
        if label == 603979785:
            return 11
        elif label == 603979784:
            return 10
        elif label == 603979783:
            return 9
        elif label == 603979782:
            return 8
        elif label == 603979781:
            return 7
        elif label == 603979780:
            return 6
        elif label == 603979779:
            return 5
        elif label == 603979778:
            return 4
        elif label == 603979777:
            return 3
        elif label == 603979776:
            return 2
        elif label == 604045311:
            return 1
        elif label == 604045310:
            return 0
        else:
            logger.debug('ERROR LABEL NOT VALID')
            return 12