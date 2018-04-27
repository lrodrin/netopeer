import logging
import os

from ncclient import manager

__author__ = "Laura Rodriguez <laura.rodriguez@cttc.cat>"
__copyright__ = "Copyright 2018, CTTC"
__license__ = "MIT License"

logger = logging.getLogger('.'.join(os.path.abspath(__name__).split('/')[1:]))


class NetopeerAPIaccessor:
    ip = '10.1.7.66'
    port = '830'
    user = 'root'
    password = 'netlabN.'

    def retrieveConfiguration(self):
        connection = manager.connect(host=self.ip, port=self.port, username=self.user, password=self.password,
                                     hostkey_verify=False, device_params={'name': 'default'}, allow_agent=False,
                                     look_for_keys=False)
        logger.debug('Connection ' + str(connection))

        configuration = connection.get_config(source='running', filter=('subtree', '<transceiver/>')).data_xml
        return configuration

# TEST
# api = NetopeerAPIaccessor()
# config = api.retrieveConfiguration()
# print(config)

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
