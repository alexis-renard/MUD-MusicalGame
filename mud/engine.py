# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

import tornado.ioloop

import threading, queue

class Engine(threading.Thread):

    def __init__(self):
        super().__init__(daemon=True)
        self._queue = queue.Queue()
        self.put = self._queue.put
        self.again = True

    def run(self):
        while self.again:
            task = self._queue.get()
            self.perform(task)

    def perform(self, task):
        meth = "perform_%s" % task["type"]
        meth = getattr(self, meth)
        meth(task)

    def perform_input(self, task):
        user    = task["user"]
        text    = task["text"]
        request = task["request"] # keep the request so that it can be reused for template rendering
        html    = request.render_string(
            "chat.html", user=user, text=text).decode("utf-8")
        def callback():
            request.output_to_all(html)
        tornado.ioloop.IOLoop.current().add_callback(callback)

ENGINE = Engine()
ENGINE.start()
