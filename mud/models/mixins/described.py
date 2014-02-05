# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .propertied import Propertied

class Described(Propertied):

    """mixin for models that have descriptions.  this provides support for
    2 kinds of descriptions: short and long.  typically long descriptions
    are intended to be used when an object is "inspected" (i.e. looked at
    carefully).

    In YAML, descriptions can be given as follows:

    they can be strings:
    
    short: a short description
    long: |
      a much longer description that
      fits on several lines.

    they can contain a list of alternatives guarded by propositions:

    long:
      - props: [+locked]
        text : the thing is closed and appears to be locked
      - props: [+closed, -locked]
        text : the thing is closed
      - props: [-closed]
        text : the thing is open

    they can contain a dictionary of alternatives retrievable by name:

    long:
      desc-locked: the thing is closed and appears to be locked
      desc-closed: the thing is closed
      desc-open  : the thing is open
    """

    #--------------------------------------------------------------------------
    # initialization
    #--------------------------------------------------------------------------

    def __init__(self, **kargs):
        super().__init__(**kargs)
        self.short = None
        self.long  = None

    #--------------------------------------------------------------------------
    # initialization from YAML data
    #--------------------------------------------------------------------------

    def init_from_yaml(self, data, world):
        super().init_from_yaml(data, world)
        if "short" in data:
            self.short = data["short"]
        if "long" in data:
            self.long = data["long"]

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

    def get_short_description(self, name=None):
        return self._get_short_description(name=name) or \
          self._get_long_description(name=name)

    def get_long_description(self, name=None):
        return self._get_long_description(name=name) or \
          self._get_short_description(name=name)

    def _get_short_description(self, name=None):
        return self._get_description_from(self.short, name=name)

    def _get_long_description(self, name=None):
        return self._get_description_from(self.long, name=name)

    def _get_description_from(self, desc, name=None):
        if isinstance(desc, str):
            return desc
        elif isinstance(desc, list):
            for d in desc:
                l = d.get("props", None)
                if (not l) or all(self.has_prop(p) for p in l):
                    return d["text"]
        else:
            return desc.get(name, None)
        
