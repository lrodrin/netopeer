from lib.COP.objects_common.jsonObject import JsonObject
from lib.COP.objects_service_topology.edgeEnd import EdgeEnd
from lib.COP.objects_common.arrayType import ArrayType
from lib.COP.objects_common.keyedArrayType import KeyedArrayType
from lib.COP.objects_common.enumType import EnumType


class Node(JsonObject):

    def __init__(self, json_struct=None):
        self.domain = ""
        self.nodetype = Nodetype(0)
        self.name = ""
        self.edgeEnd = KeyedArrayType(EdgeEnd, 'edgeEndId')
        self.nodeId = ""
        self.nodeIdType = Nodeidtype(0)
        self.underlayAbstractTopology = ArrayType.factory(str)
        super(Node, self).__init__(json_struct)


class Nodetype(EnumType):
    possible_values = ['OF', 'GMPLS', 'OF-W', 'ABSTRACT', 'OF-IOT', 'HOST', 'SDM']
    range_end = 7

    def __init__(self, initial_value):
        super(Nodetype, self).__init__(initial_value)


class Nodeidtype(EnumType):
    possible_values = ['IPv4', 'IPv6', 'DatapathID', 'MAC']
    range_end = 4

    def __init__(self, initial_value):
        super(Nodeidtype, self).__init__(initial_value)
