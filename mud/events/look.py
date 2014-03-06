# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .event import Event1

class LookEvent(Event1):
    NAME = "look"

    def get_event_templates(self):
        return self.actor.container().get_event_templates()

    def perform(self):
        if not self.actor.can_see():
            return self.failed_cannot_see()
        self.buffer_clear()
        self.buffer_inform("look.actor")
        players = []
        objects = []
        for x in self.actor.container().contents():
            if x is self.actor:
                pass
            elif x.is_player():
                players.append(x)
            else:
                objects.append(x)
        if players:
            self.buffer_inform("look-players.actor")
            self.buffer_append("<ul>")
            for x in players:
                self.buffer_peek(x)
            self.buffer_append("</ul>")
        if objects:
            self.buffer_inform("look-objects.actor")
            self.buffer_append("<ul>")
            for x in objects:
                self.buffer_peek(x)
            self.buffer_append("</ul>")
        self.actor.send_result(self.buffer_get())

    def failed_cannot_see(self):
        self.add_prop("cannot-see")
        self.buffer_clear()
        self.buffer_inform("look.failed")
        self.actor.send_result(self.buffer_get())
