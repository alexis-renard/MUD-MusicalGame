# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

import uuid
from .basic import Basic

class Identified(Basic):

    """mixin class that provides an id attribute."""

    _NEEDS_ID = True
    _UUID_IF_ID_IS_MISSING = False

    #--------------------------------------------------------------------------
    # initialization
    #--------------------------------------------------------------------------

    def __init__(self, id=None, **kargs):
        super().__init__(**kargs)
        if id is None and self._NEEDS_ID:
            if self._UUID_IF_ID_IS_MISSING:
                id = uuid.uuid4()
            else:
                raise Exception("missing id: %s" % str(kargs))
        self.id = id
        if id:
            from mud.world import WORLD
            WORLD[id] = self

    #--------------------------------------------------------------------------
    # initialization from YAML data
    #--------------------------------------------------------------------------

    def init_from_yaml(self, data, world):
        super().init_from_yaml(data, world)

    def update_from_yaml(self, data, world):
        super().update_from_yaml(data, world)

    #--------------------------------------------------------------------------
    # API for saving the dynamic parts of objects to YAML (via JSON)
    #--------------------------------------------------------------------------

    def archive_into(self, obj):
        super().archive_into(obj)
        obj["id"] = self.id
