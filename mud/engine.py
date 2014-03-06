# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

import tornado.ioloop
import threading, queue
import mud.parser

class Engine(threading.Thread):

    def __init__(self):
        super().__init__(daemon=True)
        self._queue = queue.Queue()
        self.put = self._queue.put
        self.again = True
        self.parser = mud.parser.Parser()

    def run(self):
        while self.again:
            task = self._queue.get()
            self.perform(task)

    def perform(self, task):
        meth = "perform_%s" % task["type"]
        meth = getattr(self, meth)
        meth(task)

    def perform_input(self, task):
        actor = task["player"]
        text  = task["text"]
        actor.send_echo("<pre>%s</pre>" % text)
        action,text = self.parser.parse(actor, text)
        if action:
            action.execute()
        else:
            actor.send_error("<p>hein?</p>")

#    def perform_input(self, task):
#        user    = task["user"]
#        text    = task["text"]
#        request = task["request"] # keep the request so that it can be reused for template rendering
#        html    = request.render_string(
#            "chat.html", user=user, text=text).decode("utf-8")
#        def callback():
#            request.output_to_all(html)
#        tornado.ioloop.IOLoop.current().add_callback(callback)

ENGINE = Engine()
ENGINE.start()
