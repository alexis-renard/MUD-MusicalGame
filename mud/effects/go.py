# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .effect import Effect2
from mud.events import EnterPortalEvent

class EnterPortalEffect(Effect2):
    EVENT = EnterPortalEvent
