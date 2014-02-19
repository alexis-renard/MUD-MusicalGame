# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .event import Event2

class ChangePropEvent(Event2):

    def get_event_templates(self):
        return self.actor.container().get_event_templates()

    def perform(self):
        props = self.object
        if isinstance(props, str):
            props = [props]
        self.change_props(props, self.context())
