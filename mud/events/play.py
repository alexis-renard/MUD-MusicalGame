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
        if self.object.has_prop("playable"):
            if "instrument" in self.get_props():
                for prop in self.get_props():
                    if "id" in prop:
                        #récupérer l'objet qui correspond au lieu loc
                        loc = self.resolve_object(prop)
                        self.actor.move_to(loc)
                        return(self.inform("playwith.actor"))
        return(self.play_failed())

    def resolve_object(location):
        world = mud.game.GAME.world
        loc = world.get(location)
        if loc:
            locs = [loc]
        else:
            locs = []
            for k,v in world.items():
                if isinstance(v, Containing) and \
                   not isinstance(v, Player) and \
                   k.find(self.object) != -1:
                    locs.append(v)
        return locs

    def play_failed(self): ##à implémenter plus en profondeur iflwim
        self.fail()
        self.inform("playwith.failed")


#initial
    def perform(self):
        self.inform("playwith") # de l'html
