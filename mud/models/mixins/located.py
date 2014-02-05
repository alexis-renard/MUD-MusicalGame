# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .identified import Identified

class Located(Identified):

    """mixin class for things that are located in the world, i.e. that are
    stored in containers.  A container could be a location in the world, or
    it could be something like a box, or it could a player's inventory."""

    #--------------------------------------------------------------------------
    # initialization
    #--------------------------------------------------------------------------
    
    def __init__(self, **kargs):
        super().__init__(**kargs)
        self._container = None

    #--------------------------------------------------------------------------
    # initialization from YAML data
    #--------------------------------------------------------------------------

    def init_from_yaml(self, data, world):
        super().init_from_yaml(data, world)
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
        if self._container:
            obj["container"] = self._container.id
        else:
            obj["container"] = None

    #--------------------------------------------------------------------------
    # model API
    #--------------------------------------------------------------------------

    def move_to(self, cont):
        if self._container:
            self._container.remove(self)
            self._container = None
        if cont:
            cont.add(self)
            self._container = cont

    def container(self):
        return self._container
