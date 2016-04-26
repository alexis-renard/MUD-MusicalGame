# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .event import Event2 ,Event3
from mud.models.mixins.containing import Containing
from mud.models                   import Player
import mud.game

class PlayWithEvent(Event3):
    # def __init__(self, actor, object, object2):
    #     Event2.__init__(self, actor, object2)
    #     self.object2 = object
    NAME = "playwith"

    def perform(self):
        if self.object2.has_prop("playable"):
            print("partition ok")
            if self.object.has_prop("instrument"):
                print("instrument ok")
                return(self.inform("playwith.actor"))
        return(self.play_failed())


    def play_failed(self): ##à implémenter plus en profondeur iflwim
        self.fail()
        self.inform("playwith.failed")
