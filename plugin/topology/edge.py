from lib.COP.objects_common.jsonObject import JsonObject
from lib.COP.objects_common.enumType import EnumType


class Edge(JsonObject):

    def __init__(self, json_struct=None):
        self.latency = ""
        self.name = ""
        self.edgeId = ""
        self.edgeType = Edgetype(0)
        self.switchingCap = ""
        self.metric = ""
        self.maxResvBw = ""
        self.source = ""
        self.localIfid = ""
        self.remoteIfid = ""
        self.unreservBw = ""
        self.target = ""
        super(Edge, self).__init__(json_struct)


class Edgetype(EnumType):
    possible_values = ['dwdm_edge', 'eth_edge', 'wireless_edge', 'sdm_edge']
    range_end = 4

    def __init__(self, initial_value):
        super(Edgetype, self).__init__(initial_value)
