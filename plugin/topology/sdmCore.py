from lib.COP.objects_common.jsonObject import JsonObject
from lib.COP.objects_common.keyedArrayType import KeyedArrayType
from lib.COP.objects_service_topology.frequency import Frequency


class SdmCore(JsonObject):

    def __init__(self, json_struct=None):
        self.coreId = ""
        self.availableFrequency = KeyedArrayType(Frequency, 'slotId')
        self.occupiedFrequency = KeyedArrayType(Frequency, 'slotId')
        super(SdmCore, self).__init__(json_struct)
