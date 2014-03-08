# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

import tornado.ioloop
import threading, queue
import mud.parser
import mud.game

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
        text  = task["text"].strip()
        actor.send_echo("<pre>%s</pre>" % text)
        action,text = self.parser.parse(actor, text)
        if action:
            action.execute()
        else:
            actor.send_error("<p>hein?</p>")

    def perform_save(self, task):
        actor = task["player"]
        mud.game.GAME.save()
        actor.send_info("<p>Sauvegarde effectuée!</p>")

    def perform_birth(self, task):
        actor = task["player"]
        if not actor.container():
            from mud.events.birth import BirthEvent
            BirthEvent(actor).execute()

    def perform_reset(self, task):
        actor = task["player"]
        mud.game.GAME.reset()


ENGINE = Engine()
ENGINE.start()
