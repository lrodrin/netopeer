import inspect
import json
import logging
import os
import sys
import traceback

import xmltodict
from ncclient import manager

__author__ = "Laura Rodriguez <laura.rodriguez@cttc.cat>"
__copyright__ = "Copyright 2018, CTTC"
__license__ = "MIT License"

logger = logging.getLogger('.'.join(os.path.abspath(__name__).split('/')[1:]))


def parseConfiguration(configuration):
    logger.debug(format(inspect.stack()[1]))
    logging.debug('netconfPlugin.parseConfiguration')

    configuration_dict = xmltodict.parse(configuration)
    # if 'data' in configuration_dict:
    #     del configuration_dict['data']['@xmlns']
    #     del configuration_dict['data']['@xmlns:nc']
    #
    # configuration_parsed = configuration_dict.pop('data')
    # return json.dumps(configuration_parsed, indent=4, sort_keys=True)
    return json.dumps(configuration_dict, indent=4, sort_keys=True)


class NETCONF_API:

    def __init__(self, user, password, ip, port, ):

        self.user = user
        self.password = password
        self.ip = ip
        self.port = port

    def retrieveConfiguration(self):
        logger.debug(format(inspect.stack()[1]))
        logging.debug('netconfApi.retrieveConfiguration')

        try:
            connection = manager.connect(host=self.ip, port=self.port, username=self.user,
                                         password=self.password, hostkey_verify=False,
                                         device_params={'name': 'default'}, allow_agent=False,
                                         look_for_keys=False)

            configuration = connection.get_config(source='running', filter=('subtree', '<transceiver/>')).data_xml
            configuration_json = parseConfiguration(configuration)

            return configuration_json

        except Exception as e:
            logger.error({'ERROR': str(sys.exc_info()[0]), 'VALUE': str(sys.exc_info()[1]),
                          'TRACEBACK': str(traceback.format_exc()), 'CODE': 500})
            raise e

# if __name__ == '__main__':
#     api = NETCONF_API('root', 'netlabN.', '10.1.7.84', 830)
#     print(api.retrieveConfiguration())
