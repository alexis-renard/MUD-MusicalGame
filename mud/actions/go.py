# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .action import Action2
from mud.events import EnterPortalEvent

class GoAction(Action2):
    EVENT = EnterPortalEvent
    RESOLVE_OBJECT = "resolve_for_go"
    ACTION = "go"
    RESOLVE_MAP = {}

    def resolve_object(self):
        if not self.RESOLVE_MAP:
            from mud.static import STATIC
            self.RESOLVE_MAP.update(STATIC["directions"]["normalized"])
            self.RESOLVE_MAP.update((v,k) for (k,v) in STATIC["directions"]["noun_the"].items())
            self.RESOLVE_MAP.update((v,k) for (k,v) in STATIC["directions"]["noun_at_the"].items())
        self.object = self.RESOLVE_MAP.get(self.object, None)
        return super().resolve_object()
