import logging

from ncclient import manager

__author__ = "Laura Rodriguez <laura.rodriguez@cttc.cat>"
__copyright__ = "Copyright 2018, CTTC"
__license__ = "MIT License"

# logger = logging.getLogger('.'.join(os.path.abspath(__name__).split('/')[1:]))
logging.basicConfig(filename='netconf_plugin.log', filemode='w', level=logging.DEBUG)


class NetopeerAPIaccessor:
    ip_agent_CS = '10.1.7.65'
    ip_agent_CO = '10.1.7.66'
    port = '830'
    user = 'root'
    password = 'netlabN.'

    def retrieveConfiguration(self):
        # TODO: connection and get methods
        # connection_CS = manager.connect(host=self.ip_agent_CS, port=self.port, username=self.user,
        #                                 password=self.password,
        #                                 hostkey_verify=False, device_params={'name': 'default'}, allow_agent=False,
        #                                 look_for_keys=False)
        connection_CO = manager.connect(host=self.ip_agent_CO, port=self.port, username=self.user,
                                        password=self.password,
                                        hostkey_verify=False, device_params={'name': 'default'}, allow_agent=False,
                                        look_for_keys=False)

        # logger.debug('Response connection_CS to NETCONF server ' + str(connection_CS))
        logging.debug('Response connection_CO to NETCONF server ' + str(connection_CO))

        # configuration_CO = connection_CS.get_config(source='running', filter=('subtree', '<transceiver/>')).data_xml
        configuration_CO = connection_CO.get_config(source='running', filter=('subtree', '<transceiver/>')).data_xml

        # logger.debug('Response get configuration_CO ' + str(configuration_CS))
        logging.debug('Response get configuration_CO ' + str(configuration_CO))
        #
        # return configuration_CS, configuration_CO
        return configuration_CO


# TEST
# api = NetopeerAPIaccessor()
# print(api.retrieveConfiguration())

# def retrieveNodes(self):
#     http_json = 'http://' + self.ip + ':' + str(self.port) + '/restconf/operational/opendaylight-inventory:nodes'
#
#     response = requests.get(http_json, auth=HTTPBasicAuth(self.user, self.password))
#     nodes = response.json()
#     return nodes

# def getPortListFromNode(self, nodeId, nodes=None):
#     if not nodes:
#         nodes = self.retrieveNodes()
#     for node in nodes.get('nodes')['node']:
#         for nc in node['node-connector']:
#             if self.get_datapath_id(int(nc['id'].split(':')[1])) == nodeId:
#                 return node['node-connector']
#     return None

# def getPortDetails(self, nodeId, portId):
#     http_json = 'http://' + self.ip + ':' + str(
#         self.port) + '/restconf/operational/opendaylight-inventory:nodes/node/' + str(
#         nodeId) + '/node-connector/' + str(portId)
#     logger.debug(str(http_json))
#     response = requests.get(http_json, auth=HTTPBasicAuth(self.user, self.password))
#     port = response.json()
#     logger.debug('Response %s', str(port))
#     return port

# def getdpid(self, hw_address):
#     return '00:00:' + str(hw_address).lower()

# def get_datapath_id(self, routerID):
#     routerHex = hex(routerID)
#     routerHex = routerHex[2:]  # remove 0x
#     if routerHex[-1:] == 'L':
#         routerHex = routerHex[:-1]
#     prefix_num = 16 - len(routerHex)
#     logger.debug('Router Id raw' + str(routerHex))
#     for i in range(0, prefix_num):
#         routerHex = '0' + str(routerHex)
#
#     for i in range(0, len(routerHex) / 2 - 1):
#         routerHex = routerHex[:(i + 1) * 2 + i] + ':' \
#                     + routerHex[(i + 1) * 2 + i:]
#
#     logger.debug('getDatapathID. routerID: %s , routerHex: %s', routerID, routerHex)
#     return routerHex
