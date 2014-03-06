# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .effect import Effect2
from mud.events import ChangePropEvent

class ChangePropEffect(Effect2):
    EVENT = ChangePropEvent

    def execute(self):
        self.EVENT(self.actor, self.object, self.yaml["modifs"]).execute()
