# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .action import Action2
from mud.events import EnterEvent

class GoAction(Action2):
    EVENT = EnterEvent
    RESOLVE_OBJECT = "resolve_for_go"
    ACTION = "go"
