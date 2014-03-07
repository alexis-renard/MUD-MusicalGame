# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .event import Event2

class TakeEvent(Event2):
    NAME = "take"

    def perform(self):
        if not self.object.has_prop("takable"):
            self.add_prop("object-not-takable")
            return self.failed()
        if self.object in self.actor:
            self.add_prop("object-already-in-inventory")
            return self.failed()
        self.object.move_to(self.actor)
        self.inform("take")

    def failed(self):
        self.inform("take.failed")
