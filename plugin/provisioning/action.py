from lib.COP.objects_common.jsonObject import JsonObject

__author__ = "Laura Rodriguez <laura.rodriguez@cttc.cat>"
__copyright__ = "Copyright 2018, CTTC"
__license__ = "MIT License"


class Action(JsonObject):
    def __init__(self, json_struct=None):
        self.output_phyport = ''  # Output physical port
        self.output_flood = ''  # Output FLOOD
        self.output_normal = ''  # Output NORMAL
        self.meter = ''  # METER
        self.pop_vlan = ''
        self.push_vlan = ''
        self.output_controller = ''  # VLAN id
        super(Action, self).__init__(json_struct)
