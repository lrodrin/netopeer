#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import inspect
import logging
import os, json

import xmltodict

# from TopologyManager.plugins.NETCONF_plugin.netconf_api import NetopeerAPIaccessor
from netconf_api import NetopeerAPIaccessor

__author__ = "Laura Rodriguez <laura.rodriguez@cttc.cat>"
__copyright__ = "Copyright 2018, CTTC"
__license__ = "MIT License"

logger = logging.getLogger('.'.join(os.path.abspath(__name__).split('/')[1:]))


def parseConfiguration(configuration):
    logger.debug(format(inspect.stack()[1]))
    logging.debug('netconfPlugin.parseConfiguration')

    new_configuration = xmltodict.parse(configuration)
    if 'data' in new_configuration:
        del new_configuration['data']['@xmlns']
        del new_configuration['data']['@xmlns:nc']

    configuration_parsed = new_configuration.pop('data')
    return json.dumps(configuration_parsed, indent=4, sort_keys=True)


class NETCONF_plugin(object):

    def __init__(self, **kwargs):

        for key in (
                'ctl_name',
                'ctl_addr',
                'ctl_port',
                'ctl_user',
                'ctl_password'):
            if key in kwargs:
                setattr(self, key[4:], kwargs[key])

        self.api = NetopeerAPIaccessor(self.user, self.password,
                                       self.addr, self.port)

        self.controller = kwargs['controller']

    def __str__(self):
        return self.name

    def createTopology(self):
        configuration = self.api.retrieveTopology()
        configuration_parsed = parseConfiguration(configuration)
        logger.debug('Response from {}:\n'.format(configuration_parsed))
        return configuration_parsed