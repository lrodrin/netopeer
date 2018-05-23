#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import logging
import os
import sys
import threading
import time

if sys.version_info >= (3, 0):
    import queue as Queue
else:
    import Queue

__author__ = "Laura Rodriguez <laura.rodriguez@cttc.cat>"
__copyright__ = "Copyright 2018, CTTC"
__license__ = "MIT License"

logger = logging.getLogger('.'.join(os.path.abspath(__name__).split('/')[1:]))


class FlowRequester(threading.Thread):
    def __init__(self, thread_id, req_queue, notification_queue, api):
        super(FlowRequester, self).__init__()
        self.api = api
        self.thread_id = thread_id
        self.flow_queue = req_queue
        self.notification_queue = notification_queue
        self.running = False

    def run(self):
        logger.debug('Starting thread %s', self.thread_id)
        while not self.running:
            time.sleep(0.001)
            if not self.flow_queue.empty():
                logger.debug('Request arrived')
                try:
                    request = self.flow_queue.get_nowait()
                    logger.debug(request['method'])
                    if request['method'] == 'create':
                        req = request['params']
                        logger.debug('Flow provisioning : %s', req)
                        for key in ('nodeId', 'name', 'priority', 'actions', 'matches'):
                            if key in req:
                                setattr(self, key, req[key])
                                del req[key]

                        response = self.api.insert_flow(self.nodeId, req['id'], self.name, self.priority,
                                                        self.actions, self.matches, **req)
                        self.notification_queue.put(response)
                        self.flow_queue.task_done()

                    elif request['method'] == 'remove':
                        params = request['params']
                        response = self.api.deleteFlows(params['nodeId'], params['name'])
                        self.notification_queue.put(response)
                        self.flow_queue.task_done()

                    else:
                        logger.warning('Invalid method')

                except Queue.Empty:
                    logger.debug('Accessing to a empty queue')
                    continue

        logger.debug('Stop thread %s', self.thread_id)

    def stop(self):
        self.running = True
        logger.info('Thread %s ByeBye', self.thread_id)
