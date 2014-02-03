# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .model import Model

class Container(Model):

    """a Container contains objects and/or players.  Examples of containers are:
    a box (in which you can put objects), a room (where objects can be located),
    a player (in whose inventory objects can be stored)."""

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
    # type tests for general categories of models
    #--------------------------------------------------------------------------

    def is_container(self):
        return True

    #--------------------------------------------------------------------------
    # python container API
    #--------------------------------------------------------------------------

    def __contains__(self, x):
        return x in self._contents

    def __iter__(self):
        return iter(self._contents)

    def __len__(self):
        return len(self._contents)

    #--------------------------------------------------------------------------
    # MUD container API
    #--------------------------------------------------------------------------

    def add(self, obj):
        """add an object or player to the container."""
        self._contents.add(obj)

    def remove(self, obj):
        """remove an object or player from the container."""
        self._contents.remove(obj)

    def find(self, name):
        """return the object or player present in this container and identified
        by this name, or None if no such object or player is found."""
        for x in self:
            if x.has_name(name):
                return x
