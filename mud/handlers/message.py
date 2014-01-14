# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from mud.handlers.base import BaseHandler
from mud.db.transcript import DATABASE as TRANSCRIPTS

import tornado.websocket
import tornado.escape

#==============================================================================
# handler for ajax submission of user commands
#==============================================================================

class MessageHandler(tornado.websocket.WebSocketHandler):
    opensockets = set()

    def open(self):
        user = self.get_secure_cookie("mud_player")
        if not user:
            self.close()
            return
        user = tornado.escape.json_decode(user)
        self.user = user
        self.trans = TRANSCRIPTS.lookup(user)
        self.opensockets.add(self)

    def on_close(self):
        self.opensockets.remove(self)

    def on_message(self, message):
        msg = tornado.escape.json_decode(message)
        command = msg["command"]
        command = tornado.escape.xhtml_escape(command)
        msg = {"type": "stuff", "html": command}
        html = self.render_string("message.html", message=msg)
        msg = {"type": "stuff", "html": html.decode("utf-8")}
        self.trans.append(msg)
        for ws in self.opensockets:
            ws.write_message(msg)
