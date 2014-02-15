# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .basic import Basic

class Named(Basic):

    """mixin class that provides the ability to have a name (or several).  A
    model that is named, can be identified by that name."""

    #--------------------------------------------------------------------------
    # initialization
    #--------------------------------------------------------------------------
    
    def __init__(self, **kargs):
        super().__init__(**kargs)
        self._names = set()

    #--------------------------------------------------------------------------
    # initialization from YAML data
    #--------------------------------------------------------------------------

    def init_from_yaml(self, data, world):
        super().init_from_yaml(data, world)
        if "names" in data:
            self._names.update(data["names"])
        if "name" in data:
            self._names.add(data["name"])

    def update_from_yaml(self, data, world):
        super().update_from_yaml(data, world)

    #--------------------------------------------------------------------------
    # API for saving the dynamic part of objects to YAML (via JSON)
    #--------------------------------------------------------------------------

    def archive_into(self, obj):
        super().archive_into(obj)
        obj["names"] = list(self._names)

    #--------------------------------------------------------------------------
    # model API
    #--------------------------------------------------------------------------

    def add_name(self, name):
        self._names.add(name)

    def has_name(self, name):
        return name in self._names

    def names(self):
        return iter(self._names)

    # computed property: has-name(Name)
    def _has_prop_has_name(self, name):
        return has_name(name)
