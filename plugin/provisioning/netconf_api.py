#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import logging
import os

# import requests
# from requests.auth import HTTPBasicAuth

__author__ = "Laura Rodriguez <laura.rodriguez@cttc.cat>"
__copyright__ = "Copyright 2018, CTTC"
__license__ = "MIT License"

logger = logging.getLogger('.'.join(os.path.abspath(__name__).split('/')[1:]))


class NETCONF_api:

    def __init__(
            self,
            user,
            password,
            ip,
            port,
    ):
        self.user = user
        self.password = password
        self.ip = ip
        self.port = port
        # self.url = 'http://' + ip + ':' + str(self.port) \
        #            + '/restconf/config/opendaylight-inventory:nodes/node/'

    #  FLOW OPERATIONS
    def insert_flow(self, nodeId, flowId, name, priority, actions, matches, table=0, **kwargs):

        """
        Actions: list(dict())
        Aqui la idea es recibir una estructura generica y crear el flow en funcion de los argumentos que recibimos.
        Primero cuales son comunes a todos: action, nodeId, name, priority
        """
        # TODO: Support several flows in one request
        flow = {'flow': [
            {
                'id': flowId,
                'installHw': 'true',
                'hard-timeout': 0,
                'idle-timeout': 0,
                # 'cookie_mask': 255,
                'cookie': 7,
                'flow-name': name,
                'priority': priority,
                'table_id': 0,
                'match': {},
                'instructions': {'instruction': []}
            }
        ]
        }
        flow['flow'][0]['instructions']['instruction'] = actions
        flow['flow'][0]['match'] = {}
        # TODO: Complete with all the fields and possibilities, check the fields beforehand
        for key in matches:
            if key in (
                    'in-port',
                    # 'etherType',deprecated
                    'in-phy-port',
                    'metadata',
                    'tunnel',
                    'ethernet-match',
                    'vlan-match',
                    'ip-match',
                    # l3 match
                    'arp-source-transport-address',
                    'arp-target-transport-address',
                    'arp-source-hardware-address',
                    'arp-target-hardware-address',
                    'ipv4-source',
                    'ipv4-destination',
                    # l4 match
                    'tcp-source-port',
                    'tcp-destination-port',
                    'udp-source-port',
                    'udp-destination-port'
                    'icmpv4-match',
                    'icmpv6-match',
                    'protocol-match-fields',
                    'tcp-flag-match'
                    # Incomplete list
            ):
                flow['flow'][0]['match'][key] = matches[key]
        logger.info('FLOW: ' + json.dumps(flow, indent=2))  # remove after test
        # http_json = ('http://' + self.ip + ':' + str(self.port) +
        #              '/restconf/config/opendaylight-inventory:nodes/node/'
        #              + str(nodeId) + '/table/' + str(table) + '/flow/'
        #              + str(flow['flow'][0]['id']))
        # headers = {'content-type': 'application/json'}
        logger.debug('Inserting flow: ' + str(flow))
        # response = requests.put(http_json, data=json.dumps(flow), headers=headers,
        #                         auth=HTTPBasicAuth(self.user, self.password))
        # logger.debug(response)
        # return {'name': name, 'status': response.status_code, 'content': response.content}
        return {}

    def deleteFlows(self, nodeId, flowId=None, table=0, del_table_flows=False, del_node_flows=False, **kwargs):
        if del_node_flows:
            logger.debug('Remove all flows from node %s', nodeId)
            # http_json = ('http://' + self.ip + ':' + str(self.port) +
            #              '/restconf/config/opendaylight-inventory:nodes/node/'
            #              + str(nodeId))
        elif del_table_flows:
            logger.debug('Remove all flows from table %s of node %s', table, nodeId)
            # http_json = ('http://' + self.ip + ':' + str(self.port) +
            #              '/restconf/config/opendaylight-inventory:nodes/node/'
            #              + str(nodeId) + '/table/' + str(table))
        else:
            logger.debug('Remove flow %s from node %s', flowId, nodeId)
            # http_json = ('http://' + self.ip + ':' + str(self.port) +
            #              '/restconf/config/opendaylight-inventory:nodes/node/'
            #              + str(nodeId) + '/table/' + str(table) + '/flow/' + str(flowId))

        # if kwargs.has_key('name'):
        #     name = kwargs['name']
        #     http_json += name
        # else:
        #     raise TypeError('Flow name or Id required')
        # response = requests.delete(http_json, auth=HTTPBasicAuth(self.user, self.password))
        # logger.debug('deleteFlows: %s', response)
        # return {'name': flowId, 'status': response.status_code, 'content': response.content}
        return {}

    # def insertMeter(self, nodeId, meter_id, data_rate):
    #     url1 = 'http://' + str(self.ip) + ':' + str(
    #         self.port) + '/restconf/config/opendaylight-inventory:nodes/node/' + str(nodeId) + '/meter/' + str(
    #         meter_id) + ''
    #     headers = {'content-type': 'application/json', 'Content-type': 'application/json'}
    #     data1 = '{"meter": {"meter-id": "' + str(
    #         meter_id) + '","container-name": "mymeter","meter-name":"mymeter_' + str(meter_id) + '", \
    #    "flags": "meter-kbps","meter-band-headers": {"meter-band-header": {"band-id": "1","band-rate": "' + str(
    #         data_rate) + '", \
    #    "meter-band-types": { "flags": "ofpmbt-drop" },"band-burst-size": "0","drop-rate": "' + str(
    #         data_rate) + '","drop-burst-size": "0"}}}}'
    #
    #     response = requests.put(url1, data=data1, headers=headers, auth=HTTPBasicAuth(self.user,
    #                                                                                   self.password))

    def deleteFlow(self, nodeId, name):
        logger.debug('remove flow')
        # url = self.url + '' + str(nodeId) + '/table/0/flow/' + str(name) + ''
        # response = requests.delete(url, auth=HTTPBasicAuth(self.user,
        #                                                    self.password))
        # return {'name': name, 'status': response.status_code, 'content': response.content}
        return {}

    def retrieveAllFlows(self):
        return {}
