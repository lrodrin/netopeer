#!/usr/bin/python
# -*- coding: utf-8 -*-
import importlib
import inspect
import sys
import logging
import os
if sys.version_info >= (3, 0):
    import configparser as ConfigParser
else:
    import ConfigParser

# Add current folder to path
sys.path.append(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
sys.path.append(os.path.abspath(".."))

from random import randrange
from databases.controllerDB import ControllerDB
from databases.teDB import TEDB
from databases.topologyDB import TopologyDB
from common.config import ConfigObject


import topology_controller

logger = logging.getLogger('.'.join(os.path.abspath(__name__).split('/')[1:]))

config = ConfigObject().config_storage['topology_service_settings']

__author__ = 'amll'


class TopologyManager:

    def __init__(self):
        logger.info('Initialising Topology Manager')
        self.pluginManager = NetworkPluginsManager()
        self.poolDomainIDs = list(range(0, config.getint('topology_manager',
                                   'POOL_DOMAIN_IDS')))
        config_log_dump = ''
        for each_section in config.sections():
            config_log_dump += '\n[{}]\n\n'.format(each_section).upper()
            for (each_key, each_val) in config.items(each_section):
                config_log_dump += '{key}={value}\n'.format(key=each_key, value=each_val)
        logger.debug('Configuration: {}'.format(config_log_dump))

  # REGISTER A NEW PLUGIN INSIDE TOPOLOGY MANAGER - DOES NOT IMPLY AN ACTIVE CONTROLLER.

    def registerPlugin(self, typePlugin):
        if self.pluginManager.isRegistered(typePlugin):
            logger.debug('Plugin already registered')
            pass
        else:
            self.pluginManager.addNewPlugin(typePlugin)

    def listPlugins(self):
        return self.pluginManager.getListPlugins()

  # REGISTER A NEW ACTIVE CONTROLLER OF ONE OF THE AVAILABLE PLUGINS.

    def registerController(self, settings):
        logger.debug('registerController')
        logger.debug('Callstack trace:\n\t{}'.format(inspect.stack()))
        logger.debug('kwargs:\n\t{}'.format(settings))
        domainId = settings['ctl_domain_id']
        controllerID = str(settings['ctl_type']) + '_' + str(domainId)

        if controllerID in ControllerDB.keys():
            logger.warning('Controller {} already registered'.format(controllerID))
            return None

        settings['ctrlId'] = controllerID
        settings['domainId'] = domainId
        if domainId in self.poolDomainIDs:
            del self.poolDomainIDs[self.poolDomainIDs.index(domainId)]
        pluginInfo = self.pluginManager.getPluginImpl(settings['ctl_type'])
        try:
            domainCtrl = topology_controller.TopologyController(pluginInfo, **settings)
            domainCtrl.domainId = str(domainId)
            # logger.debug('check')
            if domainCtrl.createTopology():
                topology = domainCtrl.get_topology()
                topology.topologyId = str(domainId)
                if (hasattr(domainCtrl, 'ctl_interdomain')
                        and getattr(domainCtrl, 'ctl_interdomain') == 1):
                    logger.debug('Inserting topology in TEDB :\n\t{}'.format(
                        topology)
                    )
                    TEDB.create('intdTopology', topology)
                else:
                    logger.debug('Inserting topology in TopologyDB:\n\t{}'
                                 .format(topology))
                    TopologyDB.create(topology)
                    logger.debug('Topology_created with id {}'.format(
                        TopologyDB.get(topology.topologyId).topologyId)
                    )
                    logger.debug('Registered topologies {}'.format(
                        TopologyDB.keys())
                    )
                ControllerDB.put(controllerID, domainCtrl)
            else:
                logger.error("ERROR NO TOPOLOGY")
            for value in ControllerDB.keys():
                logger.debug('KeyValue: {}'.format(value))

            return controllerID
        except (RuntimeError, IOError):
            msg = 'Controller {} has not been correctly registered'.format(
                controllerID
            )
            logger.error(msg)
            for num in self.poolDomainIDs:
                if (num < domainId and
                            self.poolDomainIDs[num + 1] < domainId):
                    self.poolDomainIDs.insert(domainId, num + 1)
            raise RuntimeError(msg)


    def getNewDomainId(self):

    # logger.debug( '\n'.join(str(p) for p in self.poolDomainIDs)

        while 1:
            temp_id = randrange(config.getint('topology_manager',
                                'POOL_DOMAIN_IDS'))
            if temp_id in self.poolDomainIDs:
                perm_id = temp_id
                del self.poolDomainIDs[self.poolDomainIDs.index(perm_id)]
                break

        return perm_id


class NetworkPluginsManager:

    def __init__(self):
        self.__listPlugins = dict()

    def addNewPlugin(self, typePlugin):

    # from PLUGINNAME.pluginName import Class PLUGIN NAME

        plugin_package = '' + typePlugin.upper() + '_plugin'
        package = 'plugins.' + plugin_package
        plugin_mod = '' + typePlugin + '_plugin'
        plugin_mainClass = plugin_package

    # Import the new plugin and creates a new instance of it .
        logger.debug(sys.version_info)
        if sys.version_info >= (3, 0):
            package = 'TopologyManager.'+package
            classToImport = importlib.import_module(package+ '.'
                                       + str(plugin_mod))

        else:            
            classToImport = importlib.import_module(package+ '.'
                                       + str(plugin_mod), plugin_mainClass)

        plugin_info = {'classToImport': classToImport, 'plugin_mainClass': plugin_mainClass}
        self.__listPlugins[typePlugin] = plugin_info

    def getPluginImpl(self, typePlugin):
        if self.isRegistered(typePlugin):
            return self.__listPlugins[typePlugin]
        else:
            raise Exception('Plugin %s is not registered.', typePlugin)

    def isRegistered(self, typePlugin):
        if typePlugin in self.__listPlugins.keys():
            return True

    def getListPlugins(self):
        return self.__listPlugins


if __name__ == '__main__':

    manager = TopologyManager()
    '''manager.registerPlugin('ryu')
    json_data = {
        'ctl_name': 'ryu1',
        'ctl_addr': '10.1.1.108',
        'ctrlPort': '8080',
        'ctl_method': 'http',
        }
    manager.registerController('ryu', **json_data)'''

    manager.registerPlugin('pce')
    json_data = {
        'ctl_name': 'pce',
        'ctl_addr': '10.1.7.84',
        'ctl_port': '8881',
        'ctl_method': 'http',
        }
    manager.registerController('pce', json_data)

    manager.registerPlugin('odl2')
    json_data = {
        'ctl_name': 'odl2',
        'ctl_addr': '10.1.7.84',
        'ctl_port': '8080',
        'ctl_method': 'http',
        'ctl_user': 'admin',
        'ctl_password': 'admin'
        }
    manager.registerController('odl2', json_data)

    # manager.registerPlugin('conf')
    # json_data = {
    #     'ctl_name': 'conf',
    #     'ctl_addr': '10.1.7.33',
    #     'ctl_port': '0000',
    #     'ctl_method': 'http',
    #     'ctl_multilayer_config_file': 'multi_topology.xml'
    #     }
    # manager.registerController('conf', json_data)

    manager.registerPlugin('netconf')
    json_data = {
        'ctl_name': 'netconf',
        'ctl_addr': '10.1.7.84',
        'ctl_port': '830',
        'ctl_method': 'ssh',
        'ctl_user': 'root',
        'ctl_password': 'netlabN.'
        }
    manager.registerController('netconf', json_data)

    #print manager.getL0Topology()
    #print manager.getL2Topology()
    print (manager.tedb.multiDomainTopology.json_serializer()['listInterDomainNodes'])
