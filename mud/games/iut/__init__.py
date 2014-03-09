# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from mud.actions import (
    GoAction, TakeAction, LookAction, InspectAction, OpenAction,
    OpenWithAction, CloseAction, TypeAction, InventoryAction,
    LightOnAction, LightOffAction, DropAction, DropInAction,
    PushAction, TeleportAction,
)

import mud.game

def make_rules():
    GAME = mud.game.GAME
    DIRS = list(GAME.static["directions"]["noun_at_the"].values())
    DIRS.extend(GAME.static["directions"]["noun_the"].values())
    DIRS.extend(GAME.static["directions"]["normalized"].keys())
    DETS = "(?:l |le |la |les |une |un |)"

    return (
        (GoAction       , r"(?:aller |)(%s)" % "|".join(DIRS)),
        (TakeAction     , r"(?:p|prendre) %s(\w+)" % DETS),
        (LookAction     , r"(?:r|regarder)"),
        (InspectAction  , r"(?:r|regarder|lire|inspecter|observer) %s(\w+)" % DETS),
        (OpenAction     , r"ouvrir %s(\w+)" % DETS),
        (OpenWithAction , r"ouvrir %s(\w+) avec %s(\w+)" % (DETS,DETS)),
        (CloseAction    , r"fermer %s(\w+)" % DETS),
        (TypeAction     , r"(?:taper|[eé]crire) (\w+)$"),
        (InventoryAction, r"(?:inventaire|inv|i)$"),
        (LightOnAction  , r"allumer %s(\w+)" % DETS),
        (LightOffAction , r"[eé]teindre %s(\w+)" % DETS),
        (DropAction     , r"(?:poser|laisser) %s(\w+)" % DETS),
        (DropInAction   , r"(?:poser|laisser) %s(\w+) (?:dans |sur |)%s(\w+)" % (DETS,DETS)),
        (PushAction     , r"(?:appuyer|pousser|presser)(?: sur|) %s(\w+)" % DETS),
        (TeleportAction , r"tele(?:porter|) (\S+)"),
    )
