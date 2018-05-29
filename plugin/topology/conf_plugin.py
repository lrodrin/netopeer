#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import logging

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

logger = logging.getLogger('.'.join(os.path.abspath(__name__).split('/')[1:]))

__author__ = "Ricard Vilalta <ricard.vilalta@cttc.cat> and Laura Rodriguez <laura.rodriguez@cttc.cat>"
__copyright__ = "Copyright 2018, CTTC"
__license__ = "MIT License"


class CONF_plugin(object):

    def __init__(self, **kwargs):
        self.controller = None
        for key in (
                'ctl_name',
                'ctl_addr',
                'ctl_port',
                'ctl_config_file'
        ):
            if key in kwargs:
                setattr(self, key[4:], kwargs[key])

        # CONFIG DATA
        self.api = CONF_API(self.addr, self.port)
        self.topology = None
        self.controller = kwargs['controller']

    def createTopology(self):
        topology = Topology()
        topology_parsed = self.parseTopology(topology)
        self.topology = topology_parsed
        return topology_parsed

    def parseTopology(self, topology):
        file_ = self.api.openFile(self.config_file)
        topology_parsed = self.parseXMLtopology(topology, file_)
        return topology_parsed

    def parseXMLtopology(self, topology, xmldoc):
        nodeList = xmldoc.getElementsByTagName('node')
        linkList = xmldoc.getElementsByTagName('link')

        for i in range(len(nodeList)):
            node = Node()
            node.nodeId = str(nodeList[i].getElementsByTagName('id')[0].childNodes[0].nodeValue)
            node.domain = str(self.controller.domainId)
            topology.nodes[node.nodeId] = node

        for i in range(len(linkList)):
            sdm = False
            source_node_value = (linkList[i].getElementsByTagName('source')[0]
                                 .childNodes[0].nodeValue
                                 )
            target_node_value = (linkList[i].getElementsByTagName('target')[0]
                                 .childNodes[0].nodeValue
                                 )

            link_id = str(source_node_value) + '_to_' + str(target_node_value)

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
                    e = DwdmEdge()
                    e.edgeType.set(1)  # DWDM Edge
                    e.delay = str(linkList[i].getElementsByTagName('delay')[0]
                                  .childNodes[0].nodeValue)
                    logger.debug('%s - DWDM Edge', link_id)
                else:
                    e = EthEdge()
                    e.edgeType.set(2)  # ETH Edge
                    logger.debug('%s - Eth Edge', link_id)
                switching_cap = 'psc'

            elif int(switching_cap_type) == 150:
                switching_cap = 'lsc'
                e = DwdmEdge()
                e.edgeType.set(1)  # DWDM Edge
                e.delay = str(linkList[i].getElementsByTagName('delay')[0]
                              .childNodes[0].nodeValue)

            elif int(switching_cap_type) == 160:
                switching_cap = 'sdm'
                e = SdmEdge()
                e.edgeType.set(4)  # SDM Edge
                e.delay = str(linkList[i].getElementsByTagName('delay')[0]
                              .childNodes[0].nodeValue)

                sdm = True

            e = self.set_parameters_edge(channel_count, dest_node, dest_port, e, i, linkList, src_node, src_port,
                                         switching_cap, topology)

            # e.source = str(src_node.nodeId)
            # e.localIfid = str(src_port)
            # e.target = str(dest_node.nodeId)
            # e.remoteIfid = str(dest_port)
            # e.metric = str(linkList[i].getElementsByTagName('te_metric')[0]
            #                .childNodes[0].nodeValue)

            # e.edgeId = str(e.source) + '_to_' + str(e.target)
            # e.switchingCap = switching_cap

            # edgeEndNotFound = False
            # try:
            #     if not topology.nodes[e.source].edgeEnd[e.localIfid]:
            #         pass

            # except:
            #     edgeEndNotFound = True

            # if not edgeEndNotFound:    # if topology.nodes[e.source].edgeEnd[e.localIfid] exists then
            #     port = EdgeEnd()
            #     port.edgeEndId = e.localIfid
            #     port.peerNodeId = topology.nodes[e.target].nodeId
            #     port.switchingCap = switching_cap
            #     topology.nodes[e.source].edgeEnd[e.localIfid] = port

            # e.maxResvBw = str(linkList[i].getElementsByTagName('max_resv_bw')[0]
            #     .childNodes[0].nodeValue)

            # e.unreservBw = str(linkList[i].getElementsByTagName('unresv_bw')[0]
            #     .getElementsByTagName('item')[0].childNodes[0].nodeValue)

            # channelsOcupied = []
            # if e.edgeType.get() == 1:
            #     logger.debug('Edge: %s',str(e))
            #     e.channels = KeyedArrayType(DwdmChannel, 'g694Id')
            #     for item in linkList[i].getElementsByTagName('channels')[0].getElementsByTagName('item'):
            #         channel = DwdmChannel()
            #         channel.g694Id = int(item.getElementsByTagName('g694_id')[0].childNodes[0].nodeValue)
            #         channel.state = int(item.getElementsByTagName('state')[0].childNodes[0].nodeValue)
            #         if channel.state == 2:
            #             logger.debug(self.__get_channel(channel.g694Id))
            #             channelsOcupied.append(self.__get_channel(channel.g694Id))

            #         e.channels[item.getElementsByTagName('g694_id'
            #                 )[0].childNodes[0].nodeValue] = channel

            #     e.bitmap = Bitmap(
            #         {
            #             'numChannels': channel_count,
            #             'arrayBits':[0] * channel_count
            #         }
            #     )
            #     for i in range(len(channelsOcupied)):
            #         e.bitmap.setChannel(channelsOcupied[i])

            topology.edges[e.edgeId] = e

        logger.debug('Composed conf topology: {}'.format(topology))
        return topology

    def refreshTopology(self, topology):
        if len(self.topology.edges) > 0:
            return self.topology
        else:
            self.parseTopology(topology)
            return topology

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

    def __str__(self):
        return self.name

    def set_parameters_edge(self, channel_count, dest_node, dest_port, e, i, linkList, src_node, src_port,
                            switching_cap, topology):
        e.source = str(src_node.nodeId)
        e.localIfid = str(src_port)
        e.target = str(dest_node.nodeId)
        e.remoteIfid = str(dest_port)
        e.metric = str(linkList[i].getElementsByTagName('te_metric')[0]
                       .childNodes[0].nodeValue)
        e.edgeId = str(e.source) + '_to_' + str(e.target)
        e.switchingCap = switching_cap
        edgeEndNotFound = False
        try:
            if not topology.nodes[e.source].edgeEnd[e.localIfid]:
                pass

        except:
            edgeEndNotFound = True
        if not edgeEndNotFound:  # if topology.nodes[e.source].edgeEnd[e.localIfid] exists then
            port = EdgeEnd()
            port.edgeEndId = e.localIfid
            port.peerNodeId = topology.nodes[e.target].nodeId
            port.switchingCap = switching_cap
            topology.nodes[e.source].edgeEnd[e.localIfid] = port
        e.maxResvBw = str(linkList[i].getElementsByTagName('max_resv_bw')[0]
                          .childNodes[0].nodeValue)
        e.unreservBw = str(linkList[i].getElementsByTagName('unresv_bw')[0]
                           .getElementsByTagName('item')[0].childNodes[0].nodeValue)
        channelsOcupied = []
        if e.edgeType.get() == 1:
            logger.debug('Edge: %s', str(e))
            e.channels = KeyedArrayType(DwdmChannel, 'g694Id')
            for item in linkList[i].getElementsByTagName('channels')[0].getElementsByTagName('item'):
                channel = DwdmChannel()
                channel.g694Id = int(item.getElementsByTagName('g694_id')[0].childNodes[0].nodeValue)
                channel.state = int(item.getElementsByTagName('state')[0].childNodes[0].nodeValue)
                if channel.state == 2:
                    logger.debug(self.__get_channel(channel.g694Id))
                    channelsOcupied.append(self.__get_channel(channel.g694Id))

                e.channels[item.getElementsByTagName('g694_id'
                                                     )[0].childNodes[0].nodeValue] = channel

            e.bitmap = Bitmap(
                {
                    'numChannels': channel_count,
                    'arrayBits': [0] * channel_count
                }
            )
            for i in range(len(channelsOcupied)):
                e.bitmap.setChannel(channelsOcupied[i])

        return e
