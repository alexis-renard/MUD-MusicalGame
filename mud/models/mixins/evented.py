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

    def _advance_event_data(self, data, context):
        while isinstance(data, list):
            data2 = None
            for datum in data:
                props = datum.get("props", None)
                if props is None:
                    data2 = datum
                    break
                if isinstance(props, str):
                    props = [prop]
                if self.has_props(props, context):
                    data2 = datum
                    break
            if data2:
                data = data2["data"]
        return data

    def _get_event_data(self, data, dotpath, context, deref_last):
        data = self.get_event_templates()
        for key in dotpath.split("."):
            data = self._advance_event_data(data, context)
            if not data:
                break
            data = data.get(key, None)
        if deref_last:
            data = self._advance_event_data(data, context)
        return data

    def world(self):
        from mud.world import WORLD
        return WORLD

    def get_event_data(self, dotpath, context, deref_last):
        return (self._get_event_data(self.get_event_templates(),
                                dotpath, context, deref_last) or
                self._get_event_data(self.world().get("events"),
                                dotpath, context, deref_last))

    def get_template(self, dotpath, context={}):
        return self.get_event_data(dotpath, context, True)

    def get_effects(self, dotpath, context={}):
        from mud.effects import Effect
        return Effect.make_effects(
            self.get_event_data(dotpath+".effects", context, False))
