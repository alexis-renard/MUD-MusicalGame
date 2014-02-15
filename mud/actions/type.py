# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .action import Action2
from mud.events import TypeEvent

class TypeAction(Action2):
    EVENT = TypeEvent
    ACTION = "type"

    def resolve_object(self):
        return self.object
