from lib.COP.objects_service_topology.edge import Edge


class SdmEdge(Edge):

    def __init__(self, json_struct=None):
        self.delay = ""  # TODO: add to schema(?)
        super(SdmEdge, self).__init__(json_struct)
