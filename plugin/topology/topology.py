from lib.COP.objects_common.jsonObject import JsonObject
from lib.COP.objects_service_topology.node import Node
from lib.COP.objects_service_topology.ethEdge import EthEdge
from lib.COP.objects_service_topology.dwdmEdge import DwdmEdge
from lib.COP.objects_service_topology.wirelessEdge import WirelessEdge
from lib.COP.objects_service_topology.sdmEdge import SdmEdge
from lib.COP.objects_common.arrayType import ArrayType
from lib.COP.objects_common.keyedArrayType import KeyedArrayType


class Topology(JsonObject):

    def __init__(self, json_struct=None):
        self.topologyId = ""
        self.underlayTopology = ArrayType.factory(str)
        self.nodes = KeyedArrayType(Node, 'nodeId')
        self.edges = KeyedArrayType((EthEdge, DwdmEdge, WirelessEdge, SdmEdge), 'edgeId', 'edgeType')
        super(Topology, self).__init__(json_struct)

    def clear(self):
        self.nodes.clear()
        self.edges.clear()
