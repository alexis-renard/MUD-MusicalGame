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
            self.add_prop("cannot-see")
            return self.failed()
        self.buffer_clear()
        self.buffer_inform("look.actor", object=self.actor.container())
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
            self.buffer_inform("look.players-intro")
            self.buffer_append("<ul>")
            for x in players:
                self.buffer_peek(x)
            self.buffer_append("</ul>")
        if objects:
            self.buffer_inform("look.objects-intro")
            self.buffer_append("<ul>")
            for x in objects:
                self.buffer_peek(x)
            self.buffer_append("</ul>")
        self.actor.send_result(self.buffer_get())

    def failed(self):
        self.buffer_clear()
        self.buffer_inform("look.failed.actor")
        self.actor.send_result(self.buffer_get())
