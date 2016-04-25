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
        print("base de la base")
        if self.object.has_prop("playable"):
            print("partition ok")
            if self.object2.has_prop("instrument"):
                print("instrument ok")
                # return(self.play_failed())
                return(self.inform("playwith.actor"))
        return(self.play_failed())


    def play_failed(self): ##à implémenter plus en profondeur iflwim
        self.fail()
        self.inform("playwith.failed")
