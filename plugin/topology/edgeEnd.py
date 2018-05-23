from lib.COP.objects_common.jsonObject import JsonObject
from lib.COP.objects_common.enumType import EnumType
from lib.COP.objects_common.keyedArrayType import KeyedArrayType

from lib.COP.objects_service_topology.sdmCore import SdmCore
from lib.COP.objects_service_topology.transceiver import Transceiver


class EdgeEnd(JsonObject):

    def __init__(self, json_struct=None):
        self.switchingCap = Switchingcap(0)
        self.edgeEndId = ""
        self.name = ""
        self.peerNodeId = ""
        self.availableCore = KeyedArrayType(SdmCore, 'coreId')
        self.availableTransceiver = Transceiver()
        # self.availableTransceiver=KeyedArrayType(Transceiver, 'transceiverId')
        super(EdgeEnd, self).__init__(json_struct)


class Switchingcap(EnumType):
    possible_values = ['lsc', 'psc', 'sdm']
    range_end = 3

    def __init__(self, initial_value):
        super(Switchingcap, self).__init__(initial_value)
