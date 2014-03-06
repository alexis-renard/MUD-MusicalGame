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
        name = data.get("name", [])
        names = data.get("names", [])
        if isinstance(name, str):
            name = [name]
        if isinstance(names, str):
            names = [names]
        names = name+names
        if names:
            self.name = names[0]
        for x in names:
            self.add_name(x)
        noun_the = data.get("noun_the")
        if noun_the is None and names:
            noun_the = "le "+self.name
        self._noun_the = noun_the
        noun_a = data.get("noun_a")
        if noun_a is None and names:
            noun_a = "un "+self.name
        self._noun_a = noun_a

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
        if name:
            self._names.add(name)

    def has_name(self, name):
        return name in self._names

    def names(self):
        return iter(self._names)

    # computed property: has-name(Name)
    def _has_prop_has_name(self, name):
        return has_name(name)

    def noun_the(self):
        return self._noun_the

    def noun_a(self):
        return self._noun_a
