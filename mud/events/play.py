# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .event import Event3
from mud.models.mixins.containing import Containing
from mud.models                   import Player
import mud.game

class PlayWithEvent(Event3):
    NAME = "play-with"

    def perform(self):
        if not self.object.has_prop("playable"):
            self.add_prop("object-not-playable")
            return self.fail()
        if self.object.has_prop("playable"):
            props = self.object2_resolved._get_props()
            print(props)
            if props[1]=="instrument":
                prop_loc = props[0]
                #récupérer l'objet qui correspond au lieu loc
                loc = this.resolve_object(prop_loc)[0]
                self.actor.move_to(loc)
        

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
        self.inform("play.failed")


#initial
    def perform(self):
        self.inform("play-with") # de l'html
