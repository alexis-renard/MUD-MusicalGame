# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

#==============================================================================
# a rule is a pair (ACTIONCLASS, PATTERN)
#==============================================================================

from mud.actions import (
    GoAction, TakeAction, LookAction, InspectAction, OpenAction,
    OpenWithAction, CloseAction, TypeAction, InventoryAction,
    LightOnAction, LightOffAction,
)
import mud.game
import re

def make_rules():
    GAME = mud.game.GAME
    DIRS = list(GAME.static["directions"]["noun_at_the"].values())
    DIRS.extend(GAME.static["directions"]["noun_the"].values())
    DIRS.extend(GAME.static["directions"]["normalized"].keys())
    DETS = "(?:l |le |la |les |une |un |)"

    return (
        (GoAction       , r"(?:aller |)(%s)$" % "|".join(DIRS)),
        (TakeAction     , r"(?:p|prendre) %s(\w+)$" % DETS),
        (LookAction     , r"(?:r|regarder)$"),
        (InspectAction  , r"(?:r|regarder|lire|inspecter|observer) %s(\w+)$" % DETS),
        (OpenAction     , r"ouvrir %s(\w+)$" % DETS),
        (OpenWithAction , r"ouvrir %s(\w+) avec %s(\w+)$" % (DETS,DETS)),
        (CloseAction    , r"fermer %s(\w+)$" % DETS),
        (TypeAction     , r"(?:taper|[eé]crire) (\w+)$"),
        (InventoryAction, r"(?:inventaire|inv|i)$"),
        (LightOnAction  , r"allumer %s(\w+)$"),
        (LightOffAction , r"[eé]teindre %s(\w+)$"),
    )

#==============================================================================
# parse(TEXT) returns a pair (ACTION,PARAMS), where ACTION is the name of the
# matching rule, and PARAMS is the list of the capturing groups from the rule's
# PATTERN.
#==============================================================================

class Parser:
    
    def __init__(self):
        self.RULES = make_rules()

    def parse(self, actor, text):
        text = " ".join(text.strip().lower().split())
        text = " ".join(text.split("'"))
        for action,pattern in self.RULES:
            pattern += "$"
            m = re.match(pattern, text)
            if m:
                return action(actor, *m.groups()),text
        return None,text
