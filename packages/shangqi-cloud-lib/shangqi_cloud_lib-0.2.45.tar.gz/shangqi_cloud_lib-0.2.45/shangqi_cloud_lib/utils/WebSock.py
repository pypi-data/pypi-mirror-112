import logging

from tornado.websocket import WebSocketHandler
from web_frame.frame.HandlerHelper import Handler

socket_map = {}


@Handler("websock类", r"/ws")
class WSHandler(WebSocketHandler):
    waiters = set()
    cache = []
    cache_size = 200

    def check_origin(self, origin):
        return True

    def get_compression_options(self):
        return {}

    def open(self):
        print('open')

    def on_close(self):
        print('close')

    def on_message(self, state):
        socket_map[state] = self
        logging.info("state的信息为{}".format(state))
