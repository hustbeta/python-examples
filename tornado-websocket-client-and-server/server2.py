#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
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
        # d = json.loads(message)
        # dispatch(d)

    def on_close(self):
        self.clients.remove(self)
        self.log('close')

if __name__ == '__main__':
    application = tornado.web.Application([
        (r'/', MainHandler),
    ])
    application.listen(8002)
    tornado.ioloop.IOLoop.instance().start()
