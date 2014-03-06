# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .model import Model
import mud.game

class Exit(Model):

    """an Exit is available at a Location, in a certain direction.  It is
    connected to a Portal which itself is connected to 1 or more other exits."""

    _NEEDS_ID = False

    #--------------------------------------------------------------------------
    # initialization
    #--------------------------------------------------------------------------

    def __init__(self, **kargs):
        super().__init__(**kargs)
        self.portal      = None
        self.location    = None
        self.direction   = None

    #--------------------------------------------------------------------------
    # initialization from YAML data
    #--------------------------------------------------------------------------

    def init_from_yaml(self, data, world):
        super().init_from_yaml(data, world)
        self.location  = world[data["location"]]
        self.direction = data.get("direction")
        self.add_name(self.direction)
        self.location.add_exit(self)

    def update_from_yaml(self, data, world):
        super().update_from_yaml(data, world)

    #--------------------------------------------------------------------------
    # API for saving the dynamic part of objects to YAML (via JSON)
    #--------------------------------------------------------------------------

    def archive_into(self, obj):
        super().archive_into(obj)

    #--------------------------------------------------------------------------
    # model API
    #--------------------------------------------------------------------------

    def is_exit(self):
        return True

    # in this design, all exits of the same portal share the same properties
    # which are stored on the portal
    def props_proxy(self):
        return self.portal

    def other_exit(self):
        return self.portal.other_exit(self)

    def get_traversal(self):
        return self.portal.get_traversal(self)

    def the_direction(self):
        return mud.game.GAME.static["directions"]["noun_the"][self.direction]
