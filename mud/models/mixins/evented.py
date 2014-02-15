# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .basic import Basic


class Evented(Basic):

    #--------------------------------------------------------------------------
    # initialization
    #--------------------------------------------------------------------------

    def __init__(self, events=None, **kargs):
        super().__init__(**kargs)
        self._event_templates = events

    #--------------------------------------------------------------------------
    # initialization from YAML data
    #--------------------------------------------------------------------------

    def init_from_yaml(self, data, world):
        super().init_from_yaml(data, world)
        if "events" in data:
            self._event_templates = data["events"]

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

    def get_event_templates(self):
        return self._event_templates

    def get_template(self, dotpath, context={}):
        data = self.get_event_templates()
        for key in dotpath.split("."):
            if not data:
                return None
            if isinstance(data, list):
                data2 = None
                for d in data:
                    l = d.get("props", None)
                    if l is None or exit.has_props(l, context):
                        data2 = d["data"]
                        break
                if data2 is None:
                    return None
                data = data2
        return data
