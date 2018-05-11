
import logging
import os
import threading
import time
import sys

if sys.version_info >= (3, 0):
    import queue as Queue
else:
    import Queue

__author__ = 'amll'


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
        logger.debug('Starting thread {}'.format(self.thread_id))
        while not self.running:
            time.sleep(0.001)
            if not self.flow_queue.empty():
                logger.debug('Request arrived')
                try:
                    request = self.flow_queue.get_nowait()
                    if request['method'] == 'create':
                        req = request['params']
                        try:
                            response = self.api.insertFlow(**req)
                        except Exception as _except:
                            raise _except
                        self.notification_queue.put(response)
                        self.flow_queue.task_done()

                    elif request['method'] == 'remove':
                        req = request['params']
                        response = self.api.deleteFlow(**req)
                        self.notification_queue.put(response)
                        self.flow_queue.task_done()

                    else:
                        logger.warning('Invalid method')
                        raise ValueError('Invalid request')

                except Queue.Empty:
                    logger.debug('Accessing to a empty queue')
                    continue
        logger.debug('Stop thread {}'.format(self.thread_id))


    def stop(self):
        self.running = True
        logger.info('Thread {} ByeBye'.format(self.thread_id))
