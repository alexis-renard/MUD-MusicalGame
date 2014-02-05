# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .propertied import Propertied

class Containing(Propertied):

    """a mixin that can contain objects and/or players.  it provides support
    for contents."""

    #--------------------------------------------------------------------------
    # initialization
    #--------------------------------------------------------------------------

    def __init__(self, **kargs):
        super().__init__(**kargs)
        self._contents = set()

    def init_from_yaml(self, data, world):
        super().init_from_yaml(data, world)

    def update_from_yaml(self, data, world):
        super().update_from_yaml(data, world)

    #--------------------------------------------------------------------------
    # API for saving the dynamic part of objects to YAML (via JSON)
    #--------------------------------------------------------------------------

    def archive_into(self, obj):
        super().archive_into(obj)

    #--------------------------------------------------------------------------
    # python container API
    #--------------------------------------------------------------------------

    def __contains__(self, x):
        return x in self._contents

    def __iter__(self):
        return iter(self._contents)

    def __len__(self):
        return len(self._contents)

    def _has_prop_empty(self):
        return not self._contents

    #--------------------------------------------------------------------------
    # MUD container API
    #--------------------------------------------------------------------------

    def add(self, obj):
        """add an object or player to the container."""
        self._contents.add(obj)

    def remove(self, obj):
        """remove an object or player from the container."""
        self._contents.remove(obj)

    def find_contents(self, name):
        """return the object or player present in this container and identified
        by this name, or None if no such object or player is found.  recursively
        look into embedded open containers."""
        if self.has_prop("closed"):
            return None
        for x in self:
            if x.has_name(name):
                return x
            if isinstance(x, Containing):
                v = x.find_contents(name)
                if v:
                    return v
        return None

    def players_in_vicinity(self):
        """return the set of players in the vicinity."""
        plr = set()
        con = self
        while con:
            for x in con:
                if x.is_player():
                    plr.add(x)
            # if the container is open, then outside players are
            # considered to be in the vicinity.  for simplicity,
            # we assume that players in nested containers are not
            # considered to be in the vicinity.
            con = None if con.has_prop("closed") else con.container()
        return plr

    def observers_in_vicinity(self, actor):
        """return the set of observers (different from the actor) that can
        see something happening in the container."""
        obs = self.players()
        obs.remove(actor)
        return obs

    def objects_in_vicinity(self):
        """return the set of objects that can be considered to be in
        the vicinity."""
        objs = set()
        con = self
        while con:
            for x in con:
                objs.add(x)
                if x.is_player():
                    objs.extend(iter(x))
            con = None if con.has_prop("closed") else con.container()
        return objs

    def find_prop_in_vicinity(self, prop):
        """return True if some object in the vicinity has property prop."""
        for x in self.objects_in_vicinity():
            if x.has_prop(prop):
                return True
        return False
