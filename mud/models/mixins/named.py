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

    GENDER = {
        "masc": "masculine",
        "m"   : "masculine",
        "fem" : "feminine" ,
        "f"   : "feminine"
    }

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
        self.gender = self.GENDER[data.get("gender", "masc")]

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

    # the following is unfortunately specific to French:

    GENDER_TO_THE = {
        "masculine": "le",
        "feminine" : "la"
    }

    def noun_the(self):
        return "%s %s" % (self.GENDER_TO_THE[self.gender],
                          self.name)

    GENDER_TO_A = {
        "masculine": "un",
        "feminine" : "une"
    }

    def noun_a(self):
        return "%s %s" % (self.GENDER_TO_A[self.gender],
                          self.name)

    GENDER_TO_HIS = {
        "masculine": "son",
        "feminine" : "sa"
    }

    def noun_his(self):
        return "%s %s" % (self.GENDER_TO_HIS[self.gender],
                          self.name)

    GENDER_TO_HER = {
        "masculine": "son",
        "feminine" : "sa"
    }

    def noun_her(self):
        return "%s %s" % (self.GENDER_TO_HER[self.gender],
                          self.name)

    GENDER_TO_E = {
        "masculine": "",
        "feminine" : "e"
    }

    def noun_e(self):
        return self.GENDER_TO_E[self.gender]
