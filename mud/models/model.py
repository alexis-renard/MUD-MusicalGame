# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

import uuid

class Model:

    """primitive base class for all models.  it provides a way for a model to
    have properties that can be tested and modified."""

    _NEEDS_ID = True
    _UUID_IF_ID_MISSING = False

    #--------------------------------------------------------------------------
    # initialization
    #--------------------------------------------------------------------------
    
    def __init__(self, id=None, **kargs):
        if id is None and self._NEEDS_ID:
            if self._UUID_IF_ID_MISSING:
                id = uuid.uuid4()
            else:
                raise Exception("missing id: %s" % str(kargs))
        self.id = id
        self._props = set()
        if id:
            from mud.world import WORLD
            WORLD[id] = self

    #--------------------------------------------------------------------------
    # initialization from YAML data
    #--------------------------------------------------------------------------

    def init_from_yaml(self, data, world):
        if "props" in data:
            self._props = set(data["props"])

    def update_from_yaml(self, data, world):
        if "props" in data:
            self._props = set(data["props"])

    #--------------------------------------------------------------------------
    # API for saving the dynamic part of objects to YAML (via JSON)
    #--------------------------------------------------------------------------

    def to_json(self):
        obj = {}
        self.archive_into(obj)
        return obj

    def archive_into(self, obj):
        obj["id"] = self.id
        obj["props"] = self._props

    #--------------------------------------------------------------------------
    # properties API
    #--------------------------------------------------------------------------

    def props_proxy(self):
        return self

    def has_prop(self, prop):
        return prop in self.props_proxy()._props

    def add_prop(self, prop):
        self.props_proxy()._props.add(prop)

    def remove_prop(self, prop):
        self.props_proxy()._props.remove(prop)

    def set_props(self, props):
        self.props_proxy()._props = set(props)

    def get_props(self):
        return list(self.props_proxy()._props)

    #--------------------------------------------------------------------------
    # type tests for general categories of models
    #--------------------------------------------------------------------------

    def is_player(self):
        return False

    def is_location(self):
        return False

    def is_container(self):
        return False
