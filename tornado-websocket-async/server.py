#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import functools
import Queue
import threading
import time

import tornado.gen
import tornado.ioloop
import tornado.web
import tornado.websocket

class MainHandler(tornado.websocket.WebSocketHandler):
    # 服务器内部的数据结构，保存所有的client连接
    clients = []

    def log(self, text):
        print datetime.datetime.now().time(), self.request.remote_ip, text

    def check_origin(self, origin):
        return True

    def get_compression_options(self):
        return {}

    def open(self):
        self.log('connected')
        self.clients.append(self)

    def on_message(self, message):
        self.log('recv: ' + message)
        self.log('async worker start')
        self.application.queue.put( (message, self._my_callback) )
        self.log('async worker finish')

    def _my_callback(self, result):
        self.log('worker result is: %s' % result)

    def on_close(self):
        self.clients.remove(self)
        self.log('close')

class ThreadWorker(threading.Thread):
    def __init__(self, queue, thread_id):
        threading.Thread.__init__(self)
        self.queue = queue
        self.thread_id = thread_id

    def run(self):
        while True:
            try:
                message, callback = self.queue.get(True, 1)
            except Queue.Empty:
                continue
            print 'DEBUG: thread %d got a message[%s]' % (self.thread_id, message)

            # cpu intensive work ...
            time.sleep(5)

            result = '%d-%s' % (self.thread_id, str(datetime.datetime.now()))
            tornado.ioloop.IOLoop.instance().add_callback(functools.partial(callback, result))
            self.queue.task_done()

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
        ]
        tornado.web.Application.__init__(self, handlers)
        self.queue = Queue.Queue()
        for i in range(5):
            print 'DEBUG: starting worker thread', i
            t = ThreadWorker(self.queue, i)
            t.setDaemon(True)
            t.start()

if __name__ == '__main__':
    application = Application()
    application.listen(8001)
    tornado.ioloop.IOLoop.instance().start()
