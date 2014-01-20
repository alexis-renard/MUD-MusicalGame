# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from mud.handlers.base import BaseHandler
from mud.db.transcript import DATABASE as TRANSCRIPTS
from mud.engine import ENGINE

import tornado.websocket
import tornado.escape
import threading

#==============================================================================
# handler for ajax submission of user commands
#==============================================================================

class WebSocketHandler(BaseHandler, tornado.websocket.WebSocketHandler):
    opensockets = set()
    lock = threading.RLock()

    def open(self):
        user = self.get_secure_cookie("mud_player")
        if not user:
            self.close()
            return
        self.player = self.get_player()
        self.opensockets.add(self)

    def on_close(self):
        self.opensockets.remove(self)

    def on_message(self, message):
        msg = tornado.escape.json_decode(message)
        msg["user"] = self.player
        msg["request"] = self
        ENGINE.put(msg)

    @staticmethod
    def output_to_all(html):
        msg = {"type":"output", "html": html}
        with WebSocketHandler.lock:
            for ws in WebSocketHandler.opensockets:
                ws.player.transcript.append(html)
                ws.write_message(msg)
