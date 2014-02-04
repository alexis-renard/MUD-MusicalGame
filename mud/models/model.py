# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

import uuid, re

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
        """returns the proxy object that actually holds the properties."""
        return self

    def has_prop(self, prop):
        """checks whether the model has the given property.

        m.has_prop("+foo")
        m.has_prop("foo")
           checks that m has property "foo".
        m.has_prop("-foo")
           checks that m doesn't have property "foo"."""
        prefix = prop[0]
        if prefix == "+":
            return self._has_prop(prop[1:])
        if prefix == "-":
            return not self._has_prop(prop[1:])
        return return self._has_prop(prop)

    def _has_prop(self, prop):
        """m.has_prop("foo") either tries m.has_prop_foo() if it exists,
        or m._has_prop_foo() if it exists, or checks if m has a property "foo"."""
        mprop = re.sub(r"[^\w]+", "_", prop)
        meth = (getattr(self,  "has_prop_"+mprop, None) or
                getattr(self, "_has_prop_"+mprop, None))
        if meth:
            return meth()
        else:
            return prop in self._get_props()

    def _get_props(self):
        return self.props_proxy()._props()

    def add_prop(self, prop):
        self._get_props().add(prop)

    def remove_prop(self, prop):
        self._get_props().remove(prop)

    def set_props(self, props):
        self.props_proxy()._props = set(props)

    def get_props(self):
        return list(self._get_props())

    #--------------------------------------------------------------------------
    # type tests for general categories of models
    #--------------------------------------------------------------------------

    def is_player(self):
        return False

    def is_location(self):
        return False

    def is_container(self):
        return False
