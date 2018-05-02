import logging
import os

import json
import xmltodict

from plugin.topology.netconf_api import NetopeerAPIaccessor

# from lib.COP.objects_service_topology.topology import Topology

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

    @staticmethod
    def createConfiguration():
        api = NetopeerAPIaccessor()
        configuration = api.retrieveConfiguration()
        return configuration

    def parseConfiguration(self, configuration):
        pass


# TEST
config = NETCONF_plugin().createConfiguration()
config_parse = (xmltodict.parse(config))
print(json.dumps(config_parse))

# def parseTopology(self, topology):
#     try:
#         odlTopologyx = self.api.retrieveTopology().get('network-topology')
#         odlTopology = odlTopologyx['topology'][0]
#         logger.debug('Topology: {}'.format(json.dumps(odlTopology)))
#         # for topo in odlTopologyx['topology']:
#         #     odlTopology = topo
#         #     logger.debug('Topology: {}'.format(odlTopology))
#         #     break
#     except IOError:
#         raise Exception
#
#     odlNodes = odlTopology['node']
#     try:
#         for odlnode in odlNodes:
#             odlnode_token= odlnode['node-id'].split(':',1)
#             logger.debug('Object {} with id {}'.format(odlnode_token[0],odlnode_token[1]))
#             if odlnode_token[0] == 'openflow':
#                 node = Node(
#                     {
#                         'name': odlnode['node-id'],
#                         'nodeId': get_datapath_id(int(odlnode_token[1]))
#                     }
#                 )
#                 # node.name = odlnode['node-id']
#                 # node.nodeId = get_datapath_id(int(odlnode['node-id'].split(':')[1]))
#                 odl_ports = [tp for tp in odlnode['termination-point']]
#                 for odl_port in odl_ports:
#                     tp_id = odl_port['tp-id'].split(':')[2]
#                     if tp_id != 'LOCAL':
#                         tp_details = self.api.getPortDetails( odlnode['node-id'], odl_port['tp-id'])
#                         port = EdgeEnd(
#                             {
#                                 'edgeEndId': tp_id,
#                                 'name': tp_details['node-connector'][0]['flow-node-inventory:name'],
#                             }
#                         )
#                         # port.edgeEndId = tp_id
#                         # port.name = tp_details['node-connector'][0]['flow-node-inventory:name']
#                         node.edgeEnd[port.edgeEndId] = port
#
#                 node.nodetype = 'OF'
#                 node.domain = str(self.controller.domainId)
#                 topology.nodes[node.nodeId] = node
#             elif odlnode_token[0] == 'host':
#                 logger.debug('Host with HwAddress {}'.format(odlnode_token[1]))
#                 pass
#             else:
#                 logger.warning('Unknown connector type: {}'.format(odlnode_token))
#         logger.debug('After node loop:\n\t{}'.format(topology))
#         if odlTopology.has_key('link'):
#             for edge in odlTopology['link']:
#                 for node in topology.nodes:
#                     if topology.nodes[node].name == edge['source']['source-node']:
#                         src_node = topology.nodes[node]
#                         src_port = edge['source']['source-tp'].split(':')[2]
#                     elif topology.nodes[node].name == edge['destination']['dest-node']:
#                         dst_node = topology.nodes[node]
#                         dst_port = edge['destination']['dest-tp'].split(':')[2]
#
#
#                 if 'src_node' in locals() and 'dst_node' in locals():
#                     linkId = str(src_node.nodeId) + '_to_' + str(dst_node.nodeId)
#                     linkId2 = str(dst_node.nodeId) + '_to_' + str(src_node.nodeId)
#                     e = EthEdge()
#                     e.source = src_node.nodeId
#                     e.localIfid = src_port
#                     e.target = dst_node.nodeId
#                     e.remoteIfid = dst_port
#                     e.edgeId = linkId
#                     e.switchingCap = 'psc'
#                     e.metric = '1'
#                     e.edgeType.set(2)
#                     e.maxResvBw = '1.0e+9'
#                     e.unreservBw = '1.0e+9'
#                     topology.nodes[e.source].edgeEnd[e.localIfid].peerNodeId = topology.nodes[e.target].nodeId
#                     topology.nodes[e.source].edgeEnd[e.localIfid].switchingCap = e.switchingCap
#                     topology.nodes[e.target].edgeEnd[e.remoteIfid].peerNodeId = topology.nodes[e.source].nodeId
#                     topology.nodes[e.target].edgeEnd[e.remoteIfid].switchingCap = e.switchingCap
#                     topology.edges[e.edgeId] = e
#
#                     ## bidirectional link
#                     e = EthEdge()
#                     e.source = dst_node.nodeId
#                     e.localIfid = dst_port
#                     e.target = src_node.nodeId
#                     e.remoteIfid = src_port
#                     e.edgeId = linkId2
#                     e.switchingCap = 'psc'
#                     e.metric = '1'
#                     e.edgeType.set(2)
#                     e.maxResvBw = '1.0e+9'
#                     e.unreservBw = '1.0e+9'
#                     topology.nodes[e.source].edgeEnd[e.localIfid].peerNodeId = topology.nodes[e.target].nodeId
#                     topology.nodes[e.source].edgeEnd[e.localIfid].switchingCap = e.switchingCap
#                     topology.nodes[e.target].edgeEnd[e.remoteIfid].peerNodeId = topology.nodes[e.source].nodeId
#                     topology.nodes[e.target].edgeEnd[e.remoteIfid].switchingCap = e.switchingCap
#                     topology.edges[e.edgeId] = e
#
#                     #cleanup variables
#                     del src_node
#                     del dst_node
#                 elif 'src_node' in locals() and not('dst_node' in locals()):
#                     del src_node
#                 elif not('src_node' in locals()) and 'dst_node' in locals():
#                     del dst_node
#                 else:
#                     pass
#
#             logger.debug('After link loop:\n\t{}'.format(topology))
#         else:
#             logger.warning('No links detected in this topology')
#
#         return topology
#
#     except Exception:
#         error = Error({'error': str(sys.exc_info()[0]),
#            'value': str(sys.exc_info()[1]),
#            'traceback': str(traceback.format_exc()),
#            'code': 500})
#         logger.error(error)
#         raise Exception(error)

# def refreshTopology(self, topology):
#     topology_parsed = self.parseTopology(topology)
#     # logger.debug('Topology: ' + str(topology_parsed))
#     return topology_parsed
