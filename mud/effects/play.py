# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .effect import Effect3
from mud.events import PlayWithEvent

class PlayWithEffect(Effect3):
    EVENT = PlayWithEvent
