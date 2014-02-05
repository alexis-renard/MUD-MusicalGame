# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

import re
from .identified import Identified

class Propertied(Identified):

    """mixin class that provides a way for a model to have properties that can
    be tested and modified."""

    #--------------------------------------------------------------------------
    # initialization
    #--------------------------------------------------------------------------
    
    def __init__(self, **kargs):
        super().__init__(**kargs)
        self._props = set()

    #--------------------------------------------------------------------------
    # initialization from YAML data
    #--------------------------------------------------------------------------

    def init_from_yaml(self, data, world):
        super().init_from_yaml(data, world)
        if "props" in data:
            self._props = set(data["props"])

    def update_from_yaml(self, data, world):
        super().update_from_yaml(data, world)
        if "props" in data:
            self._props = set(data["props"])

    #--------------------------------------------------------------------------
    # API for saving the dynamic part of objects to YAML (via JSON)
    #--------------------------------------------------------------------------

    def archive_into(self, obj):
        super().archive_into(obj)
        obj["props"] = list(self._props)

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
    # API for checking certain capabilities
    #--------------------------------------------------------------------------

    def is_key_for(self, obj):
        """return True iff this is a key for obj."""
        self.has_prop("key-for-%s" % obj.id)
