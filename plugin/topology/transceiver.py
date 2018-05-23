from lib.COP.objects_common.jsonObject import JsonObject
from lib.COP.objects_common.enumType import EnumType


class Transceiver(JsonObject):

    def __init__(self, json_struct=None):
        self.transceiverId = ""
        self.transceiverType = ""
        self.modId = ""
        self.modType = ""
        self.maxCf = ""
        self.minCf = ""
        self.maxBw = ""
        self.minBw = ""
        self.fec = ""
        self.equalization = ""
        self.monitoring = ""
        super(Transceiver, self).__init__(json_struct)
