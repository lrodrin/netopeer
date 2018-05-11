#!/usr/bin/python
# -*- coding: utf-8 -*-


import logging
import json
import os
import sys
import traceback
import time
import inspect

if sys.version_info >= (3, 0):
    import queue as Queue
else:
    import Queue

from threading import Lock
from ProvisioningManager.RYU_plugin.flow_requester import FlowRequester
from lib.COP.objects_common.error import Error
from ProvisioningManager.RYU_plugin.ryu_api import RYU_api
from common.utils import get_dpid_from_int

sys.path.append('/'.join([element for i, element in
                          enumerate(os.path.abspath(__file__).split('/'))
                          if i < len(os.path.abspath(__file__).split('/')) - 3]))

from lib.ABNO_objects.response import Response
from common.abno_cop_client import API

logger = logging.getLogger('.'.join(os.path.abspath(__name__).split('/')[1:]))

_TABLE_OUT_TUNNEL = 5
_TABLE_IN_TUNNEL = 6
_TABLE_NORMAL = 0
_TABLE_OUT_MPLS = 10


class RYU_plugin:

    # PLUGIN Initialization
    def __init__(self, **kwargs):
        for key in (
                'ctl_addr', 'ctl_port',
                'ctl_user', 'ctl_password',
                'ctl_nthreads', 'ctl_operativemode'):
            if key in kwargs:
                setattr(self, key.split('_')[1], kwargs[key])
            else:
                msg = ('{} not set'.format(key))
                logger.warning(msg)

        self.api = RYU_api(self.user, self.password,
                           self.addr, self.port)
        self.name = 'RYU'
        self.q = Queue.Queue()
        self.nofication_q = Queue.Queue()
        self.threads = list()
        self.counter = 1
        self.installed_flows = {}
        self.lock = Lock()
        self.abno_api = API()
        self.virtual_endpoints = dict()
        self.mplsLabel = [1010, 1020, 1030, 1040, 1050, 1060]  # remember to remove
        # self.remove_all_connections()

        # Open n-request processor threads
        for i in range(0, int(self.nthreads)):
            self.threads.append(FlowRequester(i, self.q, self.nofication_q, self.api))
            self.threads[i].daemon = True
            self.threads[i].start()

    def validate_endpoints(self, ingressPort, egressPort):
        logger.debug('Validating endpoints: [ingressPort {}, egressPort {}]'.format(ingressPort, egressPort))
        if ingressPort[:4] == '2011':
            if ingressPort in self.virtual_endpoints:
                ingressPort = self.virtual_endpoints[ingressPort]['pEdgeEnd']['edgeEndId']
            else:
                ingressPort = False

        if egressPort[:4] == '2011':
            if egressPort in self.virtual_endpoints:
                egressPort = self.virtual_endpoints[egressPort]['pEdgeEnd']['edgeEndId']
            else:
                egressPort = False

        return ingressPort, egressPort

    def create_connection(self, connection):
        logger.debug('Creating connection:\n\t{}'.format(connection))
        # logger.debug('Callstack trace:\n\t{}'.format(inspect.stack()))
        unservered_reqs = dict()
        try:
            self.virtual_endpoints = self.list_vEdgeEnds(connection.contextId)
            self.lock.acquire()
            if str(connection.transportLayer.layer) == 'mpls':
                response = self.create_mpls_tunnel(connection)
                if (isinstance(response, str) and
                        response.result == 'successful'):
                    self.lock.release()
                    return Response(
                        {
                            'message': 'Successful create connection operation',
                            'result': 'successful',
                            'content':
                                {
                                    'connection': connection.json_serializer(),
                                    'success_responses': []
                                }
                        })
                elif (isinstance(response, str) and
                      response.result == 'failed'):
                    self.lock.release()
                    return Response(
                        {
                            'message': 'Failed create connection operation',
                            'result': 'failed',
                            'content': response.content
                        })
                else:
                    logger.warning('BAD RESPONSE')
                    unservered_reqs = response.content
            else:
                flows_to_process = list()
                try:
                    for i in range(0, int(len(connection.path.topoComponents) / 2)):
                        ingressPort = connection.path.topoComponents[str(2 * i)].edgeEndId
                        egressPort = connection.path.topoComponents[str(2 * i + 1)].edgeEndId
                        self.validate_endpoints(ingressPort, egressPort)
                        if not ingressPort or not egressPort:
                            if str(connection.transportLayer.layer) != 'ethernet_broadcast':
                                self.lock.release()
                                error = Error(
                                    {
                                        'error': 'Internal Error',
                                        'value': 'Invalid endpoints: {},{}'.format(
                                            ingressPort, egressPort),
                                        'code': 500
                                    })
                                return Response(
                                    {
                                        'message': 'Failed create connection operation',
                                        'result': 'failed',
                                        'content': error.json_serializer()
                                    })

                        nodeId = connection.path.topoComponents[str(2 * i)].nodeId
                        dpid = get_dpid_from_int(nodeId)
                        actions = []
                        cookie = 0x1337
                        flowName = str(self.counter)
                        table_id = _TABLE_NORMAL
                        self.counter += 1
                        match = {}
                        if nodeId in self.getComputeNodes():
                            match = self.of_to_ryu_matches_converter_v1(**connection.match.json_serializer())
                        else:
                            match = self.of_to_ryu_matches_converter_v3(**connection.match.json_serializer())

                        if egressPort in self.virtual_endpoints.keys() or ingressPort in self.virtual_endpoints.keys():
                            if ingressPort in self.virtual_endpoints.keys() and egressPort in self.virtual_endpoints.keys():
                                cookie = 0x1000
                                table_id = _TABLE_OUT_TUNNEL
                                match['eth_type'] = int('0x8847', 0)
                                if 'eth_dst' not in match:
                                    match['eth_dst'] = '00:00:00:00:00:00/01:00:00:00:00:00'
                                # Uncomment below
                                # match['tunnel_id'] = int([ingressPort]['tunnel_id'])
                                match['tunnel_id'] = 771
                                actions.append(self.get_action_ryu('POP_MPLS', **{'ethertype': '0x8847'}))
                                # Uncomment below
                                # actions.append(self.get_action_ryu('SET_FIELD', **{'field':'tunnel_id',
                                #                                                    'value':int(self.virtual_endpoints[egressPort]['tunnel_id'])}))
                                actions.append(self.get_action_ryu('SET_FIELD', **{'field': 'tunnel_id',
                                                                                   'value': '1'}))
                                actions.append(self.get_action_ryu('GOTO_TABLE', **{'table_id': _TABLE_IN_TUNNEL}))
                            elif egressPort in self.virtual_endpoints.keys():
                                cookie = 0x1001
                                match['in_port'] = ingressPort
                                # Uncomment below
                                actions.append(self.get_action_ryu('SET_FIELD', **{'field': 'tunnel_id',
                                                                                   'value': int(self.virtual_endpoints[
                                                                                                    egressPort][
                                                                                                    'tunnel_id'])}))
                                # actions.append(self.get_action_ryu('SET_FIELD', **{'field': 'tunnel_id',
                                #                                                    'value': '2'}))
                                actions.append(self.get_action_ryu('GOTO_TABLE', **{'table_id': _TABLE_IN_TUNNEL}))

                            elif ingressPort in self.virtual_endpoints.keys():
                                cookie = 0x1002
                                table_id = _TABLE_OUT_TUNNEL
                                match = {}
                                match['eth_type'] = int('0x8847', 0)
                                if 'eth_dst' not in match:
                                    match['eth_dst'] = '00:00:00:00:00:00/01:00:00:00:00:00'
                                match['tunnel_id'] = int(self.virtual_endpoints[ingressPort]['tunnel_id'])
                                # match['tunnel_id'] = 772
                                actions.append(self.get_action_ryu('POP_MPLS', **{'ethertype': '0x0800'}))
                                actions.append(self.get_action_ryu('OUTPUT', **{'egressPort': egressPort}))
                        else:
                            cookie = 0x1003
                            if str(connection.transportLayer.layer) in ['ethernet']:
                                actions.append(self.get_action_ryu('OUTPUT', **{'egressPort': egressPort}))
                                match['in_port'] = ingressPort

                            elif str(connection.transportLayer.layer) == 'ethernet_broadcast':
                                actions.append(self.get_action_ryu('FLOOD'))

                        params = {
                            'name': flowName,
                            'nodeId': str(dpid),
                            'match': match,
                            'priority': '101',
                            'cookie': format(cookie),
                            'table_id': table_id,
                            'actions': actions
                        }
                        flows_to_process.append({'params': params, 'nodeId': nodeId})

                    for req in flows_to_process:
                        self.save_flow(connection, req['params'], req['nodeId'])
                        request = {'method': 'create', 'params': req['params']}
                        unservered_reqs[str(req['params']['name'])] = request
                        self.q.put(request)

                except Exception as _except:
                    error = Error(
                        {
                            'error': str(sys.exc_info()[0]),
                            'value': str(sys.exc_info()[1]),
                            'traceback': str(traceback.format_exc()),
                            'code': 500
                        })
                    logger.error(format(error))
                    self.lock.release()
                    return Response(
                        {
                            'message': 'Failed create connection operation',
                            'result': 'failed',
                            'error': error.json_serializer(),
                            'content':
                                {
                                    'connection': connection.json_serializer(),
                                    'failed_responses': unservered_reqs
                                }
                        })

            response = self.handling_responses(unservered_reqs, connection, 'create')
            self.lock.release()
            return response

        except Exception as _except:
            error = Error(
                {
                    'error': str(sys.exc_info()[0]),
                    'value': str(sys.exc_info()[1]),
                    'traceback': str(traceback.format_exc()),
                    'code': 500
                })
            logger.error(error)
            self.lock.release()
            return Response(
                {
                    'message': 'Failed create connection operation',
                    'result': 'failed',
                    'content': error.json_serializer()
                })

    def create_mpls_tunnel(self, connection):
        # FIXME: This function probably is the one overwriting MPLS label (when creating 2 or more mpls tunnels)
        try:
            cookie = 0x2773
            logger.debug('Creating mpls tunnel flow:\n\t{}'.format(connection))
            logger.debug('Current established flows\t{}'.format(self.installed_flows))
            # logger.debug('Callstack trace:\n\t{}'.format(inspect.stack()))
            unservered_reqs = dict()
            failed_responses = list()
            _range = range(0, int(len(connection.path.topoComponents) / 2))
            logger.debug('Connection mpls: {}'.format(connection.json_serializer()))
            table_id = _TABLE_NORMAL
            self.virtual_endpoints = self.list_vEdgeEnds(connection.contextId)

            if str(connection.transportLayer.action) == 'push_tag':
                actions = []
                nodeId = connection.path.topoComponents['0'].nodeId
                dpid = get_dpid_from_int(nodeId)
                components = (connection.path.topoComponents['0'], connection.path.topoComponents['1'])
                ingressPort = components[0].edgeEndId
                egressPort = components[1].edgeEndId
                flowName = str(self.counter)
                self.counter += 1
                self.validate_endpoints(ingressPort, egressPort)
                if not ingressPort or not egressPort:
                    logger.error('Not ingressPort or not egressPort from {} or {}'.format(components[0], components[1]))
                    return Response(
                        {
                            'message': 'Failed create connection operation',
                            'result': 'failed',
                            'content': Error(
                                {
                                    'error': 'Internal Error',
                                    'value': 'Invalid endpoints: ' + str(ingressPort) + ',' + str(egressPort),
                                    'code': 500
                                }).json_serializer()
                        })

                if nodeId in self.getComputeNodes():
                    match = self.of_to_ryu_matches_converter_v1(**connection.match.json_serializer())
                else:
                    match = self.of_to_ryu_matches_converter_v3(**connection.match.json_serializer())
                logger.debug('Match from json before deleting mpls_label: {}'.format(match))
                del match['mpls_label']
                if ingressPort in self.virtual_endpoints.keys() or egressPort in self.virtual_endpoints.keys():
                    if ingressPort == egressPort:
                        cookie = 0x2000
                        # When ingress = egress, the endpoints are in the same virtual port, but not necessarilly in the
                        # same physical port.
                        table_id = _TABLE_IN_TUNNEL
                        # Uncomment below
                        match['tunnel_id'] = int(self.virtual_endpoints[ingressPort]['tunnel_id'])
                        # match['tunnel_id'] = 773
                        if nodeId in self.getComputeNodes():
                            if 'dl_dst' not in match:
                                match['dl_dst'] = '00:00:00:00:00:00/01:00:00:00:00:00'
                        else:
                            if 'eth_dst' not in match:
                                match['eth_dst'] = '00:00:00:00:00:00/01:00:00:00:00:00'

                        actions.append(self.get_action_ryu('PUSH_MPLS', **{'ethertype': '0x8847'}))
                        # Ingress mpls label (electric to optical)
                        # actions.append(self.get_action_ryu('SET_FIELD', **{'field': 'mpls_label',
                        #                                                    'value': self.mplsLabel[0]}))
                        # self.mplsLabel[0] += 1
                        # Uncomment below
                        actions.append(self.get_action_ryu('SET_FIELD', **{'field': 'mpls_label',
                                                                           'value': int(connection.match.mplsLabel)}))
                        actions.append(self.get_action_ryu('OUTPUT', **{
                            'egressPort': self.virtual_endpoints[ingressPort]['pEdgeEnd']['edgeEndId']}))
                    else:
                        if ingressPort in self.virtual_endpoints.keys() and egressPort in self.virtual_endpoints.keys():
                            cookie = 0x2001
                            table_id = _TABLE_OUT_TUNNEL
                            match['eth_type'] = int('0x8847', 0)
                            if 'eth_dst' not in match:
                                match['eth_dst'] = '00:00:00:00:00:00/01:00:00:00:00:00'
                            actions.append(self.get_action_ryu('POP_MPLS', **{'ethertype': '0x0800'}))
                            actions.append(self.get_action_ryu('PUSH_MPLS', **{'ethertype': '0x8847'}))
                            # actions.append(self.get_action_ryu('SET_FIELD', **{'field': 'mpls_label',
                            #                                                    'value': self.mplsLabel[1]}))
                            # self.mplsLabel[1] += 1
                            # Uncomment below
                            actions.append(self.get_action_ryu('SET_FIELD', **{'field': 'mpls_label', 'value': int(
                                connection.match.mplsLabel)}))
                            actions.append(self.get_action_ryu('SET_FIELD', **{'field': 'tunnel_id',
                                                                               'value': int(
                                                                                   self.virtual_endpoints[egressPort][
                                                                                       'tunnel_id'])}))
                            # actions.append(self.get_action_ryu('SET_FIELD', **{'field':'tunnel_id',
                            #                                                    'value':'3'}))
                            actions.append(self.get_action_ryu('GOTO_TABLE', **{'table_id': _TABLE_IN_TUNNEL}))
                        elif ingressPort in self.virtual_endpoints.keys():
                            cookie = 0x2002
                            table_id = _TABLE_OUT_TUNNEL
                            match['eth_type'] = int('0x8847', 0)
                            if 'eth_dst' not in match:
                                match['eth_dst'] = '00:00:00:00:00:00/01:00:00:00:00:00'
                            # Uncomment below
                            match['tunnel_id'] = int(self.virtual_endpoints[ingressPort]['tunnel_id'])
                            # match['tunnel_id'] = 774
                            actions.append(self.get_action_ryu('POP_MPLS', **{'ethertype': '0x0800'}))
                            actions.append(self.get_action_ryu('PUSH_MPLS', **{'ethertype': '0x8847'}))
                            # actions.append(self.get_action_ryu('SET_FIELD', **{'field': 'mpls_label',
                            #                                                    'value': self.mplsLabel[2]}))
                            # self.mplsLabel[2] += 1
                            actions.append(self.get_action_ryu('SET_FIELD', **{'field': 'mpls_label', 'value': int(
                                connection.match.mplsLabel)}))
                            actions.append(self.get_action_ryu('OUTPUT', **{'egressPort': egressPort}))
                        elif egressPort in self.virtual_endpoints.keys():
                            cookie = 0x2003
                            match['in_port'] = ingressPort
                            actions.append(self.get_action_ryu('PUSH_MPLS', **{'ethertype': '0x8847'}))
                            # actions.append(self.get_action_ryu('SET_FIELD', **{'field': 'mpls_label',
                            #                                                    'value': self.mplsLabel[3]}))
                            # self.mplsLabel[3] += 1
                            # Uncomment below
                            actions.append(self.get_action_ryu('SET_FIELD', **{'field': 'mpls_label', 'value': int(
                                connection.match.mplsLabel)}))
                            actions.append(self.get_action_ryu('SET_FIELD', **{'field': 'tunnel_id',
                                                                               'value': int(
                                                                                   self.virtual_endpoints[egressPort][
                                                                                       'tunnel_id'])}))
                            # actions.append(self.get_action_ryu('SET_FIELD', **{'field':'tunnel_id',
                            #                                                    'value':'4'}))
                            actions.append(self.get_action_ryu('GOTO_TABLE', **{'table_id': _TABLE_IN_TUNNEL}))
                else:
                    cookie = 0x2004
                    match['in_port'] = ingressPort
                    actions.append(self.get_action_ryu('PUSH_MPLS', **{'ethertype': '0x8847'}))
                    # actions.append(self.get_action_ryu('SET_FIELD', **{'field': 'mpls_label',
                    #                                                    'value': self.mplsLabel[4]}))
                    # self.mplsLabel[4] += 1
                    # Uncomment below
                    actions.append(self.get_action_ryu('SET_FIELD', **{'field': 'mpls_label',
                                                                       'value': int(connection.match.mplsLabel)}))
                    actions.append(self.get_action_ryu('OUTPUT', **{'egressPort': egressPort}))
                logger.debug('Match:\n\t\t{}\n\tActions:\n\t\t{}'.format(match, actions))
                # logger.debug('Actions: {}'.format(actions))
                params = {
                    'name': flowName,
                    'nodeId': str(dpid),
                    'match': match,
                    'priority': '101',
                    'cookie': format(cookie),
                    'table_id': table_id,
                    'actions': actions
                }
                request = {'method': 'create', 'params': params}
                self.save_flow(connection, params, nodeId)
                unservered_reqs[str(params['name'])] = request
                self.q.put(request)
                # _range = _range[1:]

            elif str(connection.transportLayer.action) == 'pop_tag':
                actions = []
                nodeId = connection.path.topoComponents[str(len(connection.path.topoComponents) - 1)].nodeId
                dpid = get_dpid_from_int(nodeId)
                ingressPort = connection.path.topoComponents[str(len(connection.path.topoComponents) - 2)].edgeEndId
                egressPort = connection.path.topoComponents[str(len(connection.path.topoComponents) - 1)].edgeEndId
                flowName = str(self.counter)
                self.counter += 1
                self.validate_endpoints(ingressPort, egressPort)
                if not ingressPort or not egressPort:
                    return Response({'message': 'Failed create connection operation',
                                     'result': 'failed',
                                     'content': Error({'error': 'Internal Error',
                                                       'value': 'Invalid endpoints: ' + str(ingressPort) + ',' + str(
                                                           egressPort),
                                                       'code': 500}).json_serializer()})
                match = {}

                # Push a virtual endpoint egress tunnel flows
                if ingressPort in self.virtual_endpoints.keys() or egressPort in self.virtual_endpoints.keys():
                    if ingressPort == egressPort:
                        cookie = 0x2005
                        logger.debug("Adding rule for outport tunnels")
                        match['in_port'] = self.virtual_endpoints[connection.zEnd.edgeEndId]['pEdgeEnd']['edgeEndId']
                        if nodeId in self.getComputeNodes():
                            match['dl_type'] = int('0x8847', 0)
                        else:
                            match['eth_type'] = int('0x8847', 0)
                            # This mpls label is for the egress optical flow (opt->electric)
                        # match['mpls_label'] = self.mplsLabel[5]
                        # self.mplsLabel[5] += 1
                        # Uncomment below
                        match['mpls_label'] = int(connection.match.mplsLabel)
                        actions.append(self.get_action_ryu('SET_FIELD', **{'field': 'tunnel_id',
                                                                           'value': int(
                                                                               self.virtual_endpoints[egressPort][
                                                                                   'tunnel_id'])}))
                        # actions.append(self.get_action_ryu('SET_FIELD', **{'field':'tunnel_id',
                        #                                                    'value':'5'}))

                        actions.append(self.get_action_ryu('GOTO_TABLE', **{'table_id': _TABLE_OUT_TUNNEL}))
                    else:
                        if ingressPort in self.virtual_endpoints.keys() and egressPort in self.virtual_endpoints.keys():
                            cookie = 0x2006
                            table_id = _TABLE_OUT_TUNNEL
                            match['eth_type'] = int('0x8847', 0)
                            if 'eth_dst' not in match:
                                match['eth_dst'] = '00:00:00:00:00:00/01:00:00:00:00:00'
                            actions.append(self.get_action_ryu('POP_MPLS', **{'ethertype': '0x8847'}))
                            actions.append(self.get_action_ryu('POP_MPLS', **{'ethertype': '0x0800'}))
                            # actions.append(self.get_action_ryu('SET_FIELD', **{'field':'tunnel_id',
                            #                                                    'value':int(self.virtual_endpoints[egressPort]['tunnel_id'])}))
                            actions.append(self.get_action_ryu('SET_FIELD', **{'field': 'tunnel_id',
                                                                               'value': '6'}))
                            actions.append(self.get_action_ryu('GOTO_TABLE', **{'table_id': _TABLE_IN_TUNNEL}))
                        elif ingressPort in self.virtual_endpoints.keys():
                            cookie = 0x2007
                            table_id = _TABLE_OUT_TUNNEL
                            match['eth_type'] = int('0x8847', 0)
                            match['mpls_label'] = int(connection.match.mplsLabel)
                            match['tunnel_id'] = int(self.virtual_endpoints[ingressPort]['tunnel_id'])
                            # match['tunnel_id'] = 775
                            if 'eth_dst' not in match:
                                match['eth_dst'] = '00:00:00:00:00:00/01:00:00:00:00:00'
                            actions.append(self.get_action_ryu('POP_MPLS', **{'ethertype': '0x8847'}))
                            actions.append(self.get_action_ryu('POP_MPLS', **{'ethertype': '0x0800'}))
                            actions.append(self.get_action_ryu('OUTPUT', **{'egressPort': egressPort}))
                        elif egressPort in self.virtual_endpoints.keys():
                            cookie = 0x2008
                            match['in_port'] = ingressPort
                            actions.append(self.get_action_ryu('POP_MPLS', **{'ethertype': '0x0800'}))
                            # Uncomment below
                            actions.append(self.get_action_ryu('SET_FIELD', **{'field': 'tunnel_id',
                                                                               'value': int(
                                                                                   self.virtual_endpoints[egressPort][
                                                                                       'tunnel_id'])}))
                            # actions.append(self.get_action_ryu('SET_FIELD', **{'field':'tunnel_id',
                            #                                                    'value':'7'}))
                            actions.append(self.get_action_ryu('GOTO_TABLE', **{'table_id': _TABLE_IN_TUNNEL}))
                else:
                    match['in_port'] = ingressPort
                    cookie = 0x2009
                    if nodeId in self.getComputeNodes():
                        match['dl_type'] = int('0x8847', 0)
                    else:
                        match['eth_type'] = int('0x8847', 0)
                    match['mpls_label'] = int(connection.match.mplsLabel)
                    actions.append(self.get_action_ryu('POP_MPLS', **{'ethertype': '0x0800'}))
                    actions.append(self.get_action_ryu('OUTPUT', **{'egressPort': egressPort}))
                logger.debug('Match:\n\t\t{}\n\tActions:\n\t\t{}'.format(match, actions))
                params = {
                    'name': flowName,
                    'nodeId': str(dpid),
                    'match': match,
                    'priority': '101',
                    'cookie': format(cookie),
                    'table_id': table_id,
                    'actions': actions
                }
                request = {'method': 'create', 'params': params}
                self.save_flow(connection, params, nodeId)

                unservered_reqs[str(params['name'])] = request
                self.q.put(request)
                # _range = _range[:-1]

            elif str(connection.transportLayer.action) == 'forward':
                if len(_range) > 0:
                    cookie = 0x3337
                    for i in _range:
                        ingressPort = connection.path.topoComponents[str(2 * i)].edgeEndId
                        logger.debug('Ingress Port %s', str(ingressPort))
                        egressPort = connection.path.topoComponents[str(2 * i + 1)].edgeEndId
                        logger.debug('Egress Port %s', str(egressPort))
                        self.validate_endpoints(ingressPort, egressPort)
                        if not ingressPort or not egressPort:
                            return Response({'message': 'Failed create connection operation',
                                             'result': 'failed',
                                             'content': Error({'error': 'Internal Error',
                                                               'value': 'Invalid endpoints: ' + str(
                                                                   ingressPort) + ',' + str(egressPort),
                                                               'code': 500}).json_serializer()})
                        nodeId = connection.path.topoComponents[str(2 * i)].nodeId
                        logger.debug('NodeId %s', str(nodeId))
                        dpid = get_dpid_from_int(nodeId)
                        actions = []
                        flowName = str(self.counter)
                        self.counter += 1
                        match = {}
                        if nodeId in self.getComputeNodes():
                            match['dl_type'] = int('0x8847', 0)
                        else:
                            match['eth_type'] = int('0x8847', 0)

                        if egressPort in self.virtual_endpoints.keys() or ingressPort in self.virtual_endpoints.keys():
                            if egressPort in self.virtual_endpoints.keys() and ingressPort in self.virtual_endpoints.keys():
                                cookie = 0x3001
                                table_id = _TABLE_OUT_TUNNEL
                                match['eth_type'] = int('0x8847', 0)
                                if 'eth_dst' not in match:
                                    match['eth_dst'] = '00:00:00:00:00:00/01:00:00:00:00:00'
                                match['tunnel_id'] = int(self.virtual_endpoints[ingressPort]['tunnel_id'])
                                # match['tunnel_id'] = 776
                                actions.append(self.get_action_ryu('POP_MPLS', **{'ethertype': '0x8847'}))
                                actions.append(self.get_action_ryu('SET_FIELD', **{'field': 'tunnel_id',
                                                                                   'value': int(self.virtual_endpoints[
                                                                                                    egressPort][
                                                                                                    'tunnel_id'])}))
                                # actions.append(self.get_action_ryu('SET_FIELD', **{'field': 'tunnel_id',
                                #                                                    'value':'8'}))
                                actions.append(self.get_action_ryu('GOTO_TABLE', **{'table_id': _TABLE_IN_TUNNEL}))
                            elif egressPort in self.virtual_endpoints.keys():
                                cookie = 0x3002
                                match['in_port'] = ingressPort
                                match['mpls_label'] = int(connection.match.mplsLabel)
                                actions.append(self.get_action_ryu('SET_FIELD', **{'field': 'tunnel_id',
                                                                                   'value': int(self.virtual_endpoints[
                                                                                                    egressPort][
                                                                                                    'tunnel_id'])}))
                                # actions.append(self.get_action_ryu('SET_FIELD', **{'field': 'tunnel_id',
                                #                                                    'value': '9'}))
                                actions.append(self.get_action_ryu('GOTO_TABLE', **{'table_id': _TABLE_IN_TUNNEL}))

                            elif ingressPort in self.virtual_endpoints.keys():
                                cookie = 0x3003
                                table_id = _TABLE_OUT_TUNNEL
                                match['eth_type'] = int('0x8847', 0)
                                if 'eth_dst' not in match:
                                    match['eth_dst'] = '00:00:00:00:00:00/01:00:00:00:00:00'
                                # match['tunnel_id'] = int(self.virtual_endpoints[ingressPort]['tunnel_id'])
                                match['tunnel_id'] = 777
                                actions.append(self.get_action_ryu('POP_MPLS', **{'ethertype': '0x8847'}))
                                actions.append(self.get_action_ryu('OUTPUT', **{'egressPort': egressPort}))
                        else:
                            cookie = 0x3004
                            table_id = _TABLE_NORMAL
                            match['in_port'] = ingressPort
                            match['mpls_label'] = int(connection.match.mplsLabel)
                            actions.append(self.get_action_ryu('OUTPUT', **{'egressPort': egressPort}))
                        logger.debug('Match:\n\t\t{}\n\tActions:\n\t\t{}'.format(match, actions))
                        params = {
                            'name': flowName,
                            'nodeId': str(dpid),
                            'match': match,
                            'priority': '101',
                            'cookie': format(cookie),
                            'table_id': table_id,
                            'actions': actions
                        }
                        request = {'method': 'create', 'params': params}
                        self.save_flow(connection, params, nodeId)

                        unservered_reqs[str(params['name'])] = request
                        self.q.put(request)
        except Exception:
            error = Error(
                {
                    'error': str(sys.exc_info()[0]),
                    'value': str(sys.exc_info()[1]),
                    'traceback': str(traceback.format_exc()),
                    'code': 500
                })
            logger.error(format(error))
            return Response(
                {
                    'message': 'Failed create connection operation',
                    'result': 'failed',
                    'content':
                        {
                            'connection': connection.json_serializer(),
                            'failed_responses': unservered_reqs
                        }
                })

        return Response(
            {
                'message': 'Successful remove all connections operation',
                'result': 'successful',
                'content': unservered_reqs
            }
        )

    def update_connection(self, **kwargs):
        pass

    def remove_connection(self, connection, id=None):
        logger.debug('remove_connection,PARAMS:\n\tCONN\t{}\n\tID\t{}\n'
                     '\testablished flows:\t{}'.format(
            connection, id, self.installed_flows))
        try:
            if id:
                connection_id = id
            else:
                # FIXME: solve this workaround
                if type(connection) is str:
                    connection_id = connection
                else:
                    connection_id = connection.connectionId

            logger.debug('Removing connection #{}'.format(connection_id))
            unservered_reqs = dict()
            if connection_id in self.installed_flows.keys():
                self.lock.acquire()
                for nodeId in self.installed_flows[connection_id]['flows']:
                    # logger.debug('NodeId %s', nodeId)
                    for flow in self.installed_flows[connection_id]['flows'][nodeId]:
                        logger.debug('Rm flow {}_{}\n\tFLOW\t{}'.format(
                            nodeId, flow,
                            self.installed_flows[connection_id]['flows'][nodeId][flow]))
                        # logger.debug('Flow content:\n\t{}', self.installed_flows[connectionId]['flows'][nodeId][flow])
                        request = {
                            'method': 'remove',
                            'params': self.installed_flows[connection_id]['flows'][nodeId][flow]
                        }
                        unservered_reqs[request['params']['name']] = request
                        self.q.put(request)

                response = self.handling_responses(unservered_reqs, connection_id, 'remove')
                self.lock.release()
            else:
                logger.debug('Connection removed successfully')
                return Response(
                    {
                        'message': 'Successful remove connection operation',
                        'result': 'successful',
                        'content':
                            {
                                'connectionId': connection_id,
                                'success_responses': []
                            }
                    })
            return response
        except Exception:
            error = Error(
                {
                    'error': str(sys.exc_info()[0]),
                    'value': str(sys.exc_info()[1]),
                    'traceback': str(traceback.format_exc()),
                    'code': 500
                })
            logger.error(str(error))
            try:
                self.lock.release()
            except Exception:
                logger.debug('Plugin lock is already released.')

            return Response(
                {
                    'message': 'Failed remove connection operation',
                    'result': 'failed',
                    'content':
                        {
                            'connection': connection.json_serializer(),
                            'failed_responses': unservered_reqs
                        }
                })

    def remove_all_connections(self, **kwargs):
        logger.info('Removing all flows')
        total_list_flows = {}
        for conn in self.installed_flows:
            total_list_flows[conn] = self.installed_flows[conn]

        responses = dict()
        logger.debug(format(total_list_flows))
        logger.debug(format(self.installed_flows))
        for connection in total_list_flows:
            logger.debug(type(connection))
            responses[connection] = self.remove_connection(connection).json_serializer()

        logger.debug(responses)
        return Response(
            {
                'message': 'Successful remove all connections operation',
                'result': 'successful',
                'content': responses
            })

    def save_flow(self, connection, params, nodeId):
        '''
        Saves the flow into a plugin instance diccionary.
        :param connection:
        :param params:
        :param nodeId:
        :return:
        '''
        logger.debug('Saving flow: \n\tCONN\t{}\n\tPARAMS\t{},\n\tNodeID:\t{}'.format(connection, params, nodeId))
        # logger.debug('Callstack trace: \n\t{}'.format(inspect.stack()))
        flowName = params['name']
        flow_list = ''
        for conn_id in self.installed_flows.keys():
            flow_list += '\t{} :\t{}\n'.format(
                conn_id, self.installed_flows[conn_id])
        logger.debug('Current established flows:\n{}'.format(flow_list))
        if connection.connectionId not in self.installed_flows:
            # init connection DB
            self.installed_flows[connection.connectionId] = {'flows': {}}

        if nodeId not in self.installed_flows[connection.connectionId]['flows'].keys():
            # logger.debug('NodeId: '+str(nodeId))
            # logger.debug('Current nodes: '.format(self.installed_flows[connection.connectionId]['flows'].keys()))
            logger.debug('Adding {} to current nodes:\t{}'.format(
                nodeId,
                self.installed_flows[connection.connectionId]['flows'].keys()
            ))
            self.installed_flows[connection.connectionId]['flows'][nodeId] = {}

        self.installed_flows[connection.connectionId]['flows'][nodeId][flowName] = params
        logger.debug('Installed flow\n\tFLOW\t{}'.format(
            self.installed_flows[connection.connectionId]['flows'][nodeId][flowName]))

    def handling_responses(self, unservered_reqs, connection_request, method):
        """
        This method waits taking responses from the notification queue,
        checks if the all have been processed correctly, and returns True if so.
        In case, at least one of the responses had failed, it returns False
        :return boolean:
        """
        success_responses = []
        failed_responses = list()
        while int(len(unservered_reqs) - len(failed_responses)) > 0:
            logger.debug('Pending requests for method "{}": {}'.format(
                method,
                len(unservered_reqs) - len(failed_responses)
            ))
            if not self.nofication_q.empty():
                response = self.nofication_q.get()
                logger.debug('Response\n\t{}'.format(response))
                # logger.debug('unservered_reqs.keys = %s',unservered_reqs.keys())
                if str(response['name']) in unservered_reqs.keys():
                    logger.debug('Response code {status} , message {content} '
                                 'from req {name}'.format(**response)
                                 )
                    self.nofication_q.task_done()
                    if response['status'] in [200, 201, 204]:
                        success_responses.append(response['name'])
                        del unservered_reqs[response['name']]
                    else:
                        failed_responses.append(response['name'])
                else:
                    raise Exception(Error(
                        {
                            'error': 'Internal error',
                            'value': 'Invalid response ' + str(response),
                            'code': 500
                        }).json_serializer())
            time.sleep(0.001)

        if method == 'create':
            if len(failed_responses) > 0:
                logger.warning('Some create requests failed {}'.format(unservered_reqs))
                return Response(
                    {
                        'message': 'Failed create connection operation',
                        'result': 'failed',
                        'content':
                            {
                                'connection': connection_request.json_serializer(),
                                'failed_responses': failed_responses
                            }
                    }
                )
            else:
                logger.debug('Successful created connection')
                return Response(
                    {
                        'message': 'Successful create connection operation',
                        'result': 'successful',
                        'content':
                            {
                                'connection': connection_request.json_serializer(),
                                'success_responses': success_responses
                            }
                    }
                )

        elif method == 'remove':
            if len(failed_responses) > 0:
                logger.warning('Some removal requests failed {}'.format(unservered_reqs))
                return Response(
                    {
                        'message': 'Failed create connection operation',
                        'result': 'failed',
                        'content':
                            {
                                'connection': connection_request,
                                'failed_responses': failed_responses
                            }

                    }
                )
            else:
                logger.debug('Successful removed connection')
                del self.installed_flows[connection_request]
                return Response(
                    {
                        'message': 'Successful remove connection operation',
                        'result': 'successful',
                        'content':
                            {
                                'connectionId': connection_request,
                                'success_responses': success_responses
                            }
                    }
                )

        logger.warning('No valid method {}'.format(method))

    def clear(self):
        logger.debug('Clearing')
        # logger.debug('Callstack trace:\n\t{}'.format(inspect.stack()))
        try:
            self.q.join()
            for i, thread in enumerate(self.threads):
                thread.stop()
                while thread.is_alive():
                    time.sleep(0.1)

            i = 0
            while not self.nofication_q.empty():
                i += 1
                task = self.nofication_q.get()
                logger.debug('Response {} : {}'.format(i, task))
                self.nofication_q.task_done()

        except Exception:
            error = Error(
                {
                    'error': str(sys.exc_info()[0]),
                    'value': str(sys.exc_info()[1]),
                    'traceback': str(traceback.format_exc()),
                    'code': 500
                }
            )
            # print (str(error))
            logger.error(format(error))
            raise Exception(str(error))

    def getConnections(self):
        pass

    def list_vEdgeEnds(self, ctx_id):
        logger.debug('Listing virtual edge endpoints for context {}'.format(ctx_id))
        # logger.debug('Callstack trace:\n\t{}'.format(inspect.stack()))
        list_veps = self.abno_api.get_list_vEdgeEnds(**{'contextId': ctx_id})
        logger.debug('Virtual endpoints list: {} '.format(list_veps).decode())
        return list_veps

    def get_action_ryu(self, type, **kwargs):
        logger.debug('Geting action {}:\n\t{}'.format(type, kwargs))
        # logger.debug('Callstack trace:\n\t{}'.format(inspect.stack()))
        action = {}
        if type == 'OUTPUT':
            action['type'] = type
            if 'egressPort' in kwargs:
                action['port'] = kwargs['egressPort']
            else:
                err_msg = 'OUTPUT action must include "egressPort"'
                logger.error(err_msg)
                raise KeyError(err_msg)

        elif type == 'GOTO_TABLE':
            action['type'] = type
            if 'table_id' in kwargs:
                action['table_id'] = kwargs['table_id']
            else:
                err_msg = 'GOTO_TABLE action must include "table_id"'
                logger.error(err_msg)
                raise KeyError(err_msg)

        elif type == 'APPLY_ACTIONS':
            action['type'] = type
            if 'actions' in kwargs:
                action['actions'] = kwargs['actions']
            else:
                err_msg = 'APPLY_ACTIONS action must include "actions"'
                logger.error(err_msg)
                raise KeyError(err_msg)
        elif type == 'WRITE_ACTIONS':
            action['type'] = type
            if 'actions' in kwargs:
                action['actions'] = kwargs['actions']
            else:
                err_msg = 'WRITE_ACTIONS action must include "actions"'
                logger.error(err_msg)
                raise KeyError(err_msg)

        elif type == 'SET_FIELD':
            action['type'] = type
            if 'field' in kwargs and 'value' in kwargs:
                action['field'] = kwargs['field']
                action['value'] = int(kwargs['value'])
            else:
                err_msg = 'SET_FIELD action must include "field" and "value"'
                logger.error(err_msg)
                raise KeyError(err_msg)

        elif type == 'POP_MPLS':
            action['type'] = type
            if 'ethertype' in kwargs:
                if isinstance(kwargs['ethertype'], str):
                    action['ethertype'] = int(kwargs['ethertype'], 0)
                else:
                    action['ethertype'] = kwargs['ethertype']

            else:
                err_msg = 'POP_MPLS action must include "ethertype"'
                logger.error(err_msg)
                raise KeyError(err_msg)

        elif type == 'PUSH_MPLS':
            action['type'] = type
            if 'ethertype' in kwargs:
                if isinstance(kwargs['ethertype'], str):
                    action['ethertype'] = int(kwargs['ethertype'], 0)
                else:
                    action['ethertype'] = kwargs['ethertype']
            else:
                err_msg = 'PUSH_MPLS action must include "ethertype"'
                logger.error(err_msg)
                raise KeyError(err_msg)

        elif type == 'METER':
            action['type'] = type
            if 'meter_id' in kwargs:
                action['meter_id'] = kwargs['meter_id']
            else:
                err_msg = 'METER action must include "meter_id"'
                logger.error(err_msg)
                raise KeyError(err_msg)

        elif type == 'FLOOD':
            action['type'] = 'OUTPUT'
            action['port'] = 65531

        else:
            raise NotImplemented("Not implemented action type.")
        logger.debug('Result: {}'.format(action))
        return action

    def of_to_ryu_matches_converter_v3(self, **matches):
        logger.debug('Converting matches:\n\t{}'.format(matches))
        # logger.debug('Callstack trace:\n\t{}'.format(inspect.stack()))
        match_RYU = {}
        for key in [match for match in matches.keys() if (matches[match] != '' and matches[match] != 0)]:
            if key == 'inPhyPort' or key == 'inPort':
                match_RYU['in_port'] = matches[key]
            elif key == 'ethType':
                match_RYU['eth_type'] = matches[key]
            elif key == 'ethSrc':
                match_RYU['eth_src'] = matches[key]
                match_RYU['eth_type'] = 2048
            elif key == 'ethDst':
                match_RYU['eth_dst'] = matches[key]
                match_RYU['eth_type'] = 2048
            elif key == 'ipv4Src':
                match_RYU['ipv4_src'] = matches[key]
                match_RYU['eth_type'] = 2048
            elif key == 'ipv4Dst':
                match_RYU['ipv4_dst'] = matches[key]
                match_RYU['eth_type'] = 2048
            elif key == 'ipProto':
                match_RYU['ip_proto'] = matches[key]
            elif key == 'udpSrc':
                match_RYU['udp_src'] = matches[key]
                match_RYU['ip_proto'] = 17
            elif key == 'udpDst':
                match_RYU['udp_dst'] = matches[key]
                match_RYU['ip_proto'] = 17
            elif key == 'mplsLabel':
                match_RYU['mpls_label'] = matches[key]
            elif key == 'experimentalTeid':
                match_RYU['teid'] = matches[key]

        return match_RYU

    def of_to_ryu_matches_converter_v1(self, **matches):
        logger.warning('Version 1 is obsolete, it is preferable using version 3')
        match_RYU = {}
        for key in [match for match in matches.keys() if (matches[match] != '' and matches[match] != 0)]:
            if key == 'inPhyPort' or key == 'inPort':
                match_RYU['in_port'] = matches[key]
            elif key == 'ethType':
                match_RYU['dl_type'] = matches[key]
            elif key == 'ethSrc':
                match_RYU['dl_src'] = matches[key]
                match_RYU['dl_type'] = 2048
            elif key == 'ethDst':
                match_RYU['dl_dst'] = matches[key]
                match_RYU['dl_type'] = 2048
            elif key == 'ipv4Src':
                match_RYU['nw_src'] = matches[key]
            elif key == 'ipv4Dst':
                match_RYU['nw_dst'] = matches[key]
            elif key == 'ipProto':
                match_RYU['nw_proto'] = matches[key]
            elif key == 'udpSrc':
                match_RYU['tp_src'] = matches[key]
                match_RYU['nw_proto'] = 17
                match_RYU['dl_type'] = 2048
            elif key == 'udpDst':
                match_RYU['tp_dst'] = matches[key]
                match_RYU['nw_proto'] = 17
                match_RYU['dl_type'] = 2048
            elif key == 'mplsLabel':
                match_RYU['mpls_label'] = matches[key]
            elif key == 'experimentalTeid':
                match_RYU['teid'] = matches[key]

        return match_RYU

    @staticmethod
    def getComputeNodes():
        logger.debug('Getting compute nodes')
        # logger.debug('Callstack trace:\n\t{}'.format(inspect.stack()))
        listComputeNodes = []
        with open('locations.txt') as location_file:
            locations = json.load(location_file)
            for locations in locations.get('locations'):
                for field in locations:
                    listComputeNodes.append(str(locations[field]))

        return listComputeNodes
