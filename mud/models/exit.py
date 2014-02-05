# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .model import Model

class Exit(Model):

    _NEEDS_ID = False

    #--------------------------------------------------------------------------
    # initialization
    #--------------------------------------------------------------------------

    def __init__(self, **kargs):
        super().__init__(**kargs)
        self.portal      = None
        self.location    = None
        self.direction   = None
        self.destination = None

    #--------------------------------------------------------------------------
    # initialization from YAML data
    #--------------------------------------------------------------------------

    def init_from_yaml(self, data, world):
        super().init_from_yaml(data, world)
        self.location  = world[data["location"]]
        self.direction = data["direction"]
        dest = data.get("destination")
        if dest:
            self.destination = world[dest]
        self.add_name(self.direction)
        self.location.add_exit(self)

    def update_from_yaml(self, data, world):
        super().update_from_yaml(data, world)

    #--------------------------------------------------------------------------
    # API for saving the dynamic part of objects to YAML (via JSON)
    #--------------------------------------------------------------------------

    def archive_into(self, obj):
        super().archive_into(obj)

    def props_proxy(self):
        return self.portal

    #--------------------------------------------------------------------------
    # model API
    #--------------------------------------------------------------------------

    def other_exit(self):
        if self.destination:
            return self.destination
        return self.portal.other_exit(self)
