# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .model import Model

class Thing(Model):

    """a Thing is located in the world: it is stored in a container.  A
    container could be a location in the world, or it could be something
    like a box, or it could be a player's inventory.

    A Thing also has a name.  It can be identified by that name."""

    #--------------------------------------------------------------------------
    # initialization
    #--------------------------------------------------------------------------
    
    def __init__(self, **kargs):
        super().__init__(**kargs)
        self._container = None
        self._name = None

    #--------------------------------------------------------------------------
    # initialization from YAML data
    #--------------------------------------------------------------------------

    def init_from_yaml(self, data, world):
        super().init_from_yaml(data, world)
        if "name" in data:
            self._name = data["name"]
        if "container" in data:
            self.move_to(world[data["container"]])

    def update_from_yaml(self, data, world):
        super().update_from_yaml(data, world)
        if "container" in data:
            self.move_to(world[data["container"]])

    #--------------------------------------------------------------------------
    # API for saving the dynamic part of objects to YAML (via JSON)
    #--------------------------------------------------------------------------

    def archive_into(self, obj):
        super().archive_into(obj)
        obj["name"] = self._name
        if self._container:
            obj["container"] = self._container.id

    #--------------------------------------------------------------------------
    # model API
    #--------------------------------------------------------------------------

    def has_name(self, name):
        return self._name == name

    def move_to(self, cont):
        if self._container:
            self._container.remove(self)
            self._container = None
        cont.add(self)
        self._container = cont

    def container(self):
        return self._container
