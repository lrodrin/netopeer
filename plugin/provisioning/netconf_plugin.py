#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os
import sys
import time
import traceback
from threading import Lock

if sys.version_info >= (3, 0):
    import queue as Queue
else:
    import Queue

from ProvisioningManager.NETCONF_plugin.netconf_api import NETCONF_api
from ProvisioningManager.NETCONF_plugin.flow_requester import FlowRequester
from lib.ABNO_objects.response import Response
from lib.COP.objects_common.error import Error
from common.abno_cop_client import API
from common.config import ConfigObject

__author__ = "Laura Rodriguez <laura.rodriguez@cttc.cat>"
__copyright__ = "Copyright 2018, CTTC"
__license__ = "MIT License"

logger = logging.getLogger('.'.join(os.path.abspath(__name__).split('/')[1:]))

config = ConfigObject().config_storage['provisioning_service_settings']

_VIRTUAL_PREFIX = '2011'


class NETCONF_plugin:

    def __init__(self, **kwargs):
        for key in (
                'ctl_addr', 'ctl_port', 'ctl_user', 'ctl_password', 'ctl_nthreads', 'ctl_operativemode',
                'ctl_flowmeters'):
            if key in kwargs:
                setattr(self, key.split('_')[1], kwargs[key])

        # API Initialization

        self.api = NETCONF_api(self.user, self.password, self.addr,
                               self.port)
        self.name = 'NETCONF'
        # self.remove_all_connections()
        self.q = Queue.Queue()
        self.nofication_q = Queue.Queue()
        self.threads = list()
        self.counter = 1
        self.counter_meters = 1
        self.meters = {}  # DATA_RATE/ID
        self.lock = Lock()
        self.installed_flows = {}
        self.virtual_endpoints = dict()
        self.abno_api = API()

        # Open n-request processor threads
        for i in range(0, int(self.nthreads)):
            self.threads.append(FlowRequester(i, self.q, self.nofication_q, self.api))
            self.threads[i].daemon = True
            self.threads[i].start()

    def create_connection(self, connection):
        try:
            # self.lock.acquire()
            # self.virtual_endpoints = self.list_vEdgeEnds(connection.contextId)
            logger.info("Sending new connection to NETCONF: " + str(connection))
            # matches = connection.match.json_serializer()
            # unservered_reqs = {}
            #
            # for i in range(0, int(
            #         len(connection.path.topoComponents) / 2)):  # There are 2 ports (ingress, egress) per node
            #     ingressPort = connection.path.topoComponents[str(2 * i)].edgeEndId
            #     egressPort = connection.path.topoComponents[str(2 * i + 1)].edgeEndId
            #
            #     ingressPort, egressPort = self.validate_endpoints(ingressPort, egressPort)
            #
            #     action = ''
            #     if ingressPort != '':
            #         matches['inPhyPort'] = ingressPort
            #     else:
            #         if 'inPhyPort' in matches.keys():
            #             logger.debug('Removing old inPort match.')
            #             del matches['inPhyPort']
            #
            #     if (str(connection.transportLayer.layer) != 'ethernet_broadcast') and (
            #             egressPort == '' or ingressPort == ''):
            #         logger.debug('Invalid flow, ingress or egress port does not exists')
            #         continue
            #     else:
            #         node_id_cop = connection.path.topoComponents[str(2 * i)].nodeId
            #         nodeId = 'openflow:' + str(dpid_hexs2dec(node_id_cop))  # Formato ODL (openflow:HW_ADDR)
            #         # flowName = str(connection.id) + '_' + nodeId + '_action:_' + connection.action
            #         flowName = str(nodeId) + '_' + str(self.counter)
            #         flowId = str(nodeId) + '_' + str(self.counter)
            #         self.counter += 1
            #         # Convert OpenFlow standard table matches, to custom Opendaylight matches.
            #         ODL_matches = self.of_to_odl_matches_converter(matches)
            #
            #         if str(connection.transportLayer.layer) != 'ethernet_broadcast':
            #             action = Action()
            #             action.output_phyport = egressPort
            #         else:
            #             action = Action()
            #             action.output_flood = True
            #
            #         logger.debug('Actions before odl filter %s', str(action))
            #         actions = self.of_to_odl_action_converter(action.json_serializer())
            #         logger.debug('Actions after odl filter %s', str(actions))
            #         logger.debug('Node to push flows : ' + str(nodeId)
            #                      + ', ingressPort = ' + str(ingressPort)
            #                      + ', egressPort = ' + str(egressPort))
            #
            #         NODE_INFO = {'id': flowId, 'nodeId': nodeId,
            #                      'priority': 6,
            #                      'name': flowName,
            #                      'actions': actions,
            #                      'matches': ODL_matches}
            #         params = NODE_INFO
            #         logger.debug('Input params : %s', str(params))
            #         request = {'method': 'create', 'params': params}
            #         unservered_reqs[str(params['name'])] = request
            #         self.save_flow(connection, params, nodeId)
            #
            #         self.q.put(request)
            #
            # response = self.handling_responses(unservered_reqs, connection, 'create')
            # self.lock.release()
            # return response
        except Exception:
            error = Error({'error': str(sys.exc_info()[0]),
                           'value': str(sys.exc_info()[1]),
                           'traceback': str(traceback.format_exc()),
                           'code': 500})
            logger.error(error)
            raise Exception(error)

    def update_connection(self, **kwargs):
        pass

    def remove_connection(self, connection, id=None):
        try:
            logger.info("Sending new connection to remove in NETCONF: " + str(connection))
            # logger.debug('Current established flows: ' + str(self.installed_flows))
            # self.lock.acquire()
            # if id:
            #     connectionId = id
            # else:
            #     connectionId = connection.connectionId
            #
            # logger.debug('Remove connection: %s ', str(connectionId))
            # unservered_reqs = dict()
            # if connectionId in self.installed_flows.keys():
            #     for nodeId in self.installed_flows[connectionId]['flows']:
            #         logger.debug('NodeId %s', nodeId)
            #         for flow in self.installed_flows[connectionId]['flows'][nodeId]:
            #             logger.debug('FlowId %s_%s' % (nodeId, flow))
            #             logger.debug('Flow: %s', self.installed_flows[connectionId]['flows'][nodeId][flow])
            #             request = {'method': 'remove',
            #                        'params': self.installed_flows[connectionId]['flows'][nodeId][flow]}
            #             unservered_reqs[request['params']['name']] = request
            #             self.q.put(request)
            #
            # response = self.handling_responses(unservered_reqs, connectionId, 'remove')
            # self.lock.release()
            # return response
        except Exception:
            error = Error({'error': str(sys.exc_info()[0]),
                           'value': str(sys.exc_info()[1]),
                           'traceback': str(traceback.format_exc()),
                           'code': 500})
            logger.error(error)
            raise Exception(error)

    def remove_all_connections(self, **kwargs):
        logger.info(' Removing Old flows ')
        # total_list_flows = {}
        # for conn in self.installed_flows:
        #     total_list_flows[conn] = self.installed_flows[conn]
        #
        # responses = dict()
        # for connection in total_list_flows:
        #     responses[connection] = self.remove_connection(None, id=connection).json_serializer()
        #
        # return Response({'message': 'Successful remove all connections operation',
        #                  'result': 'successful',
        #                  'content': responses})

    # def save_flow(self, connection, params, nodeId):
    # flowName = params['name']
    # logger.debug('Current established flows: ' + str(self.installed_flows))
    # if connection.connectionId not in self.installed_flows:
    #     logger.debug('Init db')
    #     self.installed_flows[connection.connectionId] = {'flows': {}}
    #
    # if nodeId not in self.installed_flows[connection.connectionId]['flows'].keys():
    #     logger.debug('NodeId: ' + str(nodeId))
    #     logger.debug('Current nodes: ' + str(self.installed_flows[connection.connectionId]['flows'].keys()))
    #     self.installed_flows[connection.connectionId]['flows'][nodeId] = {}
    #
    # self.installed_flows[connection.connectionId]['flows'][nodeId][flowName] = params.copy()
    # logger.debug('Installed flow: ' + str(self.installed_flows[connection.connectionId]['flows'][nodeId][flowName]))

    # This method waits take the responses from the notification queue, checks if the all
    # have been processed correctly, and returns True if so. In case, at least one of the
    # responses had failed, it returns False.
    def handling_responses(self, unservered_reqs, connection_request, method):
        # success_responses = []
        # failed_responses = list()
        logger.debug('method : %s', method)
        # logger.debug('Number pending requests : %s', int(len(unservered_reqs) - len(failed_responses)))
        # logger.debug('Unreserved_reqs %s', unservered_reqs.keys())
        # while int(len(unservered_reqs) - len(failed_responses)) > 0:
        #     if not self.nofication_q.empty():
        #         response = self.nofication_q.get()
        #         logger.debug('Unreserved_reqs %s', unservered_reqs.keys())
        #         if str(response['name']) in unservered_reqs.keys():
        #             logger.debug('Response code %s , message %s from req %s' % (
        #             response['status'], response['content'], response['name']))
        #             self.nofication_q.task_done()
        #             if response['status'] in [200, 201, 204]:
        #                 success_responses.append(response['name'])
        #                 del unservered_reqs[response['name']]
        #             else:
        #                 failed_responses.append(response['name'])
        #         else:
        #             logger.debug('Response! %s', str(response['name']))
        #             raise ValueError('Invalid request')
        #     time.sleep(0.001)
        #
        # if method == 'create':
        #     if len(failed_responses) > 0:
        #         logger.warning('One or more flow requests have failed %s', str(unservered_reqs))
        #         return Response({'message': 'Failed create connection operation', 'result': 'failed',
        #                          'content': {'connection': connection_request.json_serializer(),
        #                                      'failed_responses': failed_responses}})
        #     else:
        #         logger.debug('Successful created connection')
        #         return Response({'message': 'Successful create connection operation', 'result': 'successful',
        #                          'content': {'connection': connection_request.json_serializer(),
        #                                      'success_responses': success_responses}})
        # elif method == 'remove':
        #     if len(failed_responses) > 0:
        #         logger.warning('One or more flow requests have failed %s', str(unservered_reqs))
        #         return Response({'message': 'Failed create connection operation', 'result': 'failed',
        #                          'content': {'connectionId': connection_request,
        #                                      'failed_responses': failed_responses}})
        #     else:
        #         logger.debug('Successful removed connection')
        #         del self.installed_flows[connection_request]
        #         return Response({'message': 'Successful remove connection operation', 'result': 'successful',
        #                          'content': {'connectionId': connection_request,
        #                                      'success_responses': success_responses}})

        logger.warning('No valid method %s', method)

    # def list_vEdgeEnds(self, ctx_id):
    #     list_veps = self.abno_api.get_list_vEdgeEnds(**{'contextId': ctx_id})
    #     logger.debug('Virtual endpoints list: %s ', str(list_veps))
    #     return list_veps

    # def validate_endpoints(self, ingressPort, egressPort):
    #     logger.debug('Original ingressPort %s, egressPort %s' % (ingressPort, egressPort))
    #     if ingressPort[:len(_VIRTUAL_PREFIX)] == _VIRTUAL_PREFIX:
    #         if ingressPort in self.virtual_endpoints:
    #             a = self.virtual_endpoints[ingressPort]['pEdgeEnd']['edgeEndId']
    #         else:
    #             a = False
    #     else:
    #         a = ingressPort
    #
    #     if egressPort[:len(_VIRTUAL_PREFIX)] == _VIRTUAL_PREFIX:
    #         if egressPort in self.virtual_endpoints:
    #             b = self.virtual_endpoints[egressPort]['pEdgeEnd']['edgeEndId']
    #         else:
    #             b = False
    #     else:
    #         b = egressPort
    #
    #     logger.debug('After validation: ingressPort %s, egressPort %s' % (a, b))
    #
    #     return a, b

    # def clear(self):
    #     try:
    #         self.q.join()
    #         for thread in self.threads:
    #             thread.stop()
    #             while thread.is_alive():
    #                 time.sleep(0.1)
    #
    #         i = 0
    #         while not self.nofication_q.empty():
    #             i += 1
    #             task = self.nofication_q.get()
    #             logger.debug('Response %s : %s' % (i, str(task)))
    #             self.nofication_q.task_done()
    #
    #     except Exception:
    #         raise sys.exc_info()

    # def of_to_odl_action_converter(self, actions):
    #     # TODO: Complete action list
    #     '''
    #     Template:
    #     {
    #         'flow': [
    #             {
    #                 'id': str()
    #                 [...]
    #                 'instructions': {
    #                     'instruction': [
    #                         {
    #                             'order': 'int32',
    #                             <instructionType>:(list() or dict())
    #                             }
    #                         }
    #                     ]
    #                 }
    #             }
    #         ]
    #     }
    #
    #     :param actions:
    #     :return:
    #     '''
    #     odl2_actions = []
    #
    #     for i, action in enumerate(actions):
    #         if action == 'output_phyport':
    #             instruction = {
    #                 'order': 0,
    #                 'apply-actions': {
    #                     'action': [
    #                         {
    #                             'order': 0,
    #                             'output-action': {
    #                                 'output-node-connector': actions[action],
    #                                 'max-length': 60
    #                             }
    #                         }
    #                     ]
    #                 }
    #             }
    #             odl2_actions.append(instruction)
    #         elif action == 'output_flood':
    #             instruction = {
    #                 'order': 1,
    #                 'apply-actions': {
    #                     'action': [
    #                         {
    #                             'order': 0,
    #                             'output-action': {
    #                                 'output-node-connector': 'FLOOD',
    #                                 'max-length': 60
    #                             }
    #                         }
    #                     ]
    #                 }
    #             }
    #             odl2_actions.append(instruction)
    #         elif action == 'meter':
    #             instruction = {
    #                 'order': 2,
    #                 'meter': {
    #                     'meter-id': actions[action]
    #                 }
    #             }
    #             odl2_actions.append(instruction)
    #         else:
    #             raise Exception('Invalid Action: ' + action + ', ODL2 does not support it (yet).')
    #
    #     return odl2_actions

    # def of_to_odl_matches_converter(self, matches):
    #     # TODO: Complete match list
    #     '''
    #     Some flow requests won't work unless they have the required fields, i.e., if the ipv4Src match is used,
    #     the flow won't work unless ethType = 2048 (0x0800) is specified.
    #
    #     Template:
    #     {
    #         'flow': [
    #             {
    #                 'id': str()
    #                 [...]
    #                 'match': {
    #                     '<matchType>': '<value>'
    #                 }
    #             }
    #         ]
    #     }
    #
    #     :param matches:
    #     :return:
    #     '''
    #     match_ODL = {}
    #     for key in [match for match in matches.keys() if (matches[match] != '' and matches[match] != 0)]:
    #         if key == 'inPhyPort' or key == 'inPort':
    #             match_ODL['in-port'] = matches[key]
    #         elif key == 'ethType':
    #             if 'ethernet-match' not in match_ODL:
    #                 match_ODL['ethernet-match'] = {}
    #             match_ODL['ethernet-match']['ethernet-type'] = {}
    #             match_ODL['ethernet-match']['ethernet-type']['type'] = int(matches[key], 16)
    #         elif key == 'ethSrc':
    #             if 'ethernet-match' not in match_ODL:
    #                 match_ODL['ethernet-match'] = {}
    #             match_ODL['ethernet-match']['ethernet-source'] = {}
    #             match_ODL['ethernet-match']['ethernet-source']['address'] = matches[key]
    #             if 'ethernet-type' not in match_ODL['ethernet-match']:
    #                 match_ODL['ethernet-match']['ethernet-type'] = {}
    #             match_ODL['ethernet-match']['ethernet-type']['type'] = 2048
    #         elif key == 'ethDst':
    #             if 'ethernet-match' not in match_ODL:
    #                 match_ODL['ethernet-match'] = {}
    #             match_ODL['ethernet-match']['ethernet-destination'] = {}
    #             match_ODL['ethernet-match']['ethernet-destination']['address'] = matches[key]
    #             if 'ethernet-type' not in match_ODL['ethernet-match']:
    #                 match_ODL['ethernet-match']['ethernet-type'] = {}
    #             match_ODL['ethernet-match']['ethernet-type']['type'] = 2048
    #         elif key == 'ipv4Src':
    #             match_ODL['ipv4-source'] = matches[key]
    #         elif key == 'ipv4Dst':
    #             match_ODL['ipv4-destination'] = matches[key]
    #         elif key == 'tcpSrc':
    #             match_ODL['tcp-source-port'] = matches[key]
    #             if 'ethernet-match' not in match_ODL:
    #                 match_ODL['ethernet-match'] = {}
    #             match_ODL['ethernet-match']['ethernet-type'] = {}
    #             match_ODL['ethernet-match']['ethernet-type']['type'] = 2048
    #             match_ODL['ip-match'] = {}
    #             match_ODL['ip-match']['ip-protocol'] = 6
    #         elif key == 'tcpDst':
    #             match_ODL['tcp-destination-port'] = matches[key]
    #             if 'ethernet-match' not in match_ODL:
    #                 match_ODL['ethernet-match'] = {}
    #             match_ODL['ethernet-match']['ethernet-type'] = {}
    #             match_ODL['ethernet-match']['ethernet-type']['type'] = 2048
    #             match_ODL['ip-match'] = {}
    #             match_ODL['ip-match']['ip-protocol'] = 6
    #         elif key == 'udpSrc':
    #             match_ODL['udp-source-port'] = matches[key]
    #             if 'ethernet-match' not in match_ODL:
    #                 match_ODL['ethernet-match'] = {}
    #             match_ODL['ethernet-match']['ethernet-type'] = {}
    #             match_ODL['ethernet-match']['ethernet-type']['type'] = 2048
    #             match_ODL['ip-match'] = {}
    #             match_ODL['ip-match']['ip-protocol'] = 17
    #         elif key == 'udpDst':
    #             match_ODL['udp-destination-port'] = matches[key]
    #             if 'ethernet-match' not in match_ODL:
    #                 match_ODL['ethernet-match'] = {}
    #             match_ODL['ethernet-match']['ethernet-type'] = {}
    #             match_ODL['ethernet-match']['ethernet-type']['type'] = 2048
    #             match_ODL['ip-match'] = {}
    #             match_ODL['ip-match']['ip-protocol'] = 17
    #         elif key == 'vlanVid':
    #             if 'ethernet-match' not in match_ODL:
    #                 match_ODL['ethernet-match'] = {}
    #             match_ODL['ethernet-match']['ethernet-type'] = {}
    #             match_ODL['ethernet-match']['ethernet-type']['type'] = 33024
    #             match_ODL['vlan-match'] = {}
    #             match_ODL['vlan-match']['vlan-id'] = {}
    #             match_ODL['vlan-match']['vlan-id']['vlan-id-present'] = True
    #             match_ODL['vlan-match']['vlan-id']['vlan-id'] = matches[key]
    #         elif key == 'mplsLabel':
    #             match_ODL['protocol-match-fields'] = {}
    #             match_ODL['protocol-match-fields']['mpls-label'] = matches[key]
    #
    #     return match_ODL

# def dpid_hexs2dec(dpid):
#     """Translates a dpid string into a decimal ID integer"""
#     string_dpid = dpid.replace(':', '')
#     int_dpid = int(string_dpid, base=16)
#     return int_dpid
#
#
# def dpid_dec2hexs(nodeId):
#     """Translates dpid(OVS ID) from decimal ID stored in ODL-DB to hexadecimal
#      pairs separated with ":". Returns a string with format XX:XX:...XX:XX
#     """
#     routerHex = hex(nodeId)
#     routerHex = routerHex[2:]  # remove 0x
#     if routerHex[-1:] == 'L':
#         routerHex = routerHex[:-1]
#     prefix_num = 16 - len(routerHex)
#     logger.debug('Router Id raw' + str(routerHex))
#     for i in range(0, prefix_num):
#         routerHex = '0' + str(routerHex)
#
#     for i in range(0, int(len(routerHex) / 2) - 1):
#         routerHex = routerHex[:(i + 1) * 2 + i] + ':' \
#                     + routerHex[(i + 1) * 2 + i:]
#
#     # logger.debug('getDatapathID. nodeId: %s , routerHex: %s', nodeId, routerHex)
#     return routerHex
