from lib.COP.objects_common.jsonObject import JsonObject


class Frequency(JsonObject):

    def __init__(self, json_struct=None):
        self.slotId = ""
        self.gridType = ""
        self.adjustGranularity = ""
        self.numChannel = ""
        self.numSlotWidth = ""
        super(Frequency, self).__init__(json_struct)
