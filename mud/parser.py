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
from mud.static import STATIC

DIRS = list(STATIC["directions"]["noun_at_the"].values())
DIRS.extend(STATIC["directions"]["noun_the"].values())
DIRS.extend(STATIC["directions"]["normalized"].keys())
DETS = "(?:l |le |la |les |une |un |)"

RULES = (
    (ActionGo       , r"(?:aller |)(%s)$" % "|".join(DIRS)),
    (ActionTake     , r"prendre %s(\w+)$" % DETS),
    (ActionLook     , r"regarder$"),
    (ActionInspect  , r"(?:regarder|lire|inspecter|observer) %s(\w+)$" % DETS),
    (ActionOpen     , r"ouvrir %s(\w+)$" % DETS),
    (ActionOpenWith , r"ouvrir %s(\w+) avec %s(\w+)$" % (DETS,DETS)),
    (ActionClose    , r"fermer %s(\w+)$" % DETS),
    (ActionType     , r"(?:taper|[eé]crire) (\w+)$"),
    (ActionInventory, r"(?:inventaire|inv|i)$"),
    (LightOnAction  , r"allumer %s(\w+)$"),
    (LightOffAction , r"[eé]teindre %s(\w+)$"),
)

#==============================================================================
# parse(TEXT) returns a pair (ACTION,PARAMS), where ACTION is the name of the
# matching rule, and PARAMS is the list of the capturing groups from the rule's
# PATTERN.
#==============================================================================

def parse(actor, text):
    text = " ".join(text.strip().lower().split())
    text = " ".join(text.split("'"))
    for action,pattern in rules:
        pattern += "$"
        m = pattern.match(text)
        if m:
            return action(actor, *m.groups())
    return None,text
