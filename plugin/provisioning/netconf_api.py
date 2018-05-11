#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import logging
import os, sys
import json

sys.path.append('/'.join([element for i, element in
                          enumerate(os.path.abspath(__file__).split('/'))
                          if i < len(os.path.abspath(__file__).split('/')) - 3]))

logger = logging.getLogger('.'.join(os.path.abspath(__name__).split('/')[1:]))


class RYU_api:

    def __init__(self, user, password, ip, port, ):

        self.user = user
        self.password = password
        self.ip = ip
        self.port = port
        self.url = 'http://' + ip + ':' + str(self.port) + '/stats/'

        self.dpid = []

        # Retrieve controlled dpids
        url = self.url + 'switches'
        # headers = {'content-type': 'application/json'}
        response = requests.get(url,
                                # headers=headers,
                                auth=(self.user, self.password))
        logger.debug(response.content)
        logger.debug(response.text)

        for dpid in json.loads(response.text):
            logger.debug("Controlled dpid %s", dpid)
            self.dpid.append(dpid)

        # for dpid in self.dpid :
        # self.deleteAllFlows(dpid)

    def insertFlow(self, **kwargs):
        flow = {}
        for key in ('nodeId', 'name', 'match', 'priority', 'actions', 'table_id', 'cookie'):
            if key in kwargs:
                flow[key] = kwargs[key]

        flow['dpid'] = flow['nodeId']
        del flow['nodeId']
        # flow['cookie'] = 1
        http_json = '' + self.url + 'flowentry/add'
        headers = {'content-type': 'application/json'}

        logger.debug("Sending to: {} - data: {}".format(http_json, flow))
        response = requests.post(http_json, data=json.dumps(flow),
                                 headers=headers,
                                 auth=(self.user, self.password))
        logger.debug(
            'Response code {} , message {} from req {}'.format(response.status_code, response.content, kwargs['name']))
        return {'name': kwargs['name'], 'status': response.status_code, 'content': response.content}

    def deleteFlow(self, **kwargs):
        flow = {}
        for key in ('nodeId', 'name', 'match', 'priority', 'actions', 'table_id'):
            if key in kwargs:
                flow[key] = kwargs[key]

        flow['dpid'] = flow['nodeId']
        del flow['nodeId']
        flow['cookie'] = 1
        http_json = '' + self.url + 'flowentry/delete_strict'
        headers = {'content-type': 'application/json'}
        logger.debug("Sending to: {} - data: {}".format(http_json, flow))
        response = requests.post(http_json, data=json.dumps(flow),
                                 headers=headers,
                                 auth=(self.user,
                                       self.password))
        logger.debug(
            'Response code {} , message {} from req {}'.format(response.status_code, response.content, kwargs['name']))
        return {'name': kwargs['name'], 'status': response.status_code, 'content': response.content}

    def deleteAllFlows(self, dpid):
        http_json = self.url + 'flowentry/clear/' + str(dpid)
        logger.debug("deleting all flows for dpid %s: %s", dpid, http_json)
        response = requests.delete(http_json, auth=(self.user,
                                                    self.password))
        logger.debug("Status code: %s", response.status_code)
        return True

    def retrieveAllFlows(self):
        flow_dict = {}
        for dpid in self.dpid:
            http_json = self.url + 'flow/' + str(dpid)

            response = requests.get(http_json, auth=(self.user,
                                                     self.password))
            allFlows = response.json()
            flow_dict[dpid] = allFlows

        logger.debug("Retrieved flow: %s", flow_dict)
        return flow_dict
