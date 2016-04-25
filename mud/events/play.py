# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .event import Event3
from mud.models.mixins.containing import Containing
from mud.models                   import Player
import mud.game

class PlayWithEvent(Event3):
    NAME = "playwith"

    def perform(self):
        if not self.object.has_prop("playable"):
            self.add_prop("object-not-playable")
            print(1)
        if self.object.has_prop("playable"):
            print(2)
            return(self.inform("playwith.failed"))
            print(2.1)
            if "instrument" in self.object.get_props():
                return(self.inform("playwith.actor"))
                print(3)
        return(self.play_failed())

    def play_failed(self):
        self.fail()
        self.inform("playwith.failed")
