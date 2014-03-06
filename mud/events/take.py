# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .event import Event2

class TakeEvent(Event2):
    NAME = "take"

    def perform(self):
        if not self.object.has_prop("takable"):
            return self.inform("take.failed")
        self.object.move_to(self.actor)
        self.inform("take")
