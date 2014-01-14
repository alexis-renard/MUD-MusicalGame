# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

#==============================================================================
# a rule is a pair (ACTION, PATTERN)
#==============================================================================

rules = []

#==============================================================================
# parse(TEXT) returns a pair (ACTION,PARAMS), where ACTION is the name of the
# matching rule, and PARAMS is the list of the capturing groups from the rule's
# PATTERN.
#==============================================================================

def parse(text):
    text = " ".join(text.strip().lower().split())
    for action,pattern in rules:
        m = pattern.match(text)
        if m:
            return action,m.groups()
    return None,text

#==============================================================================
# example of rules for english commands. they can be activated as follows:
#
#     mud.parser.rules.extend(mud.parser.ENGLISH_RULES)
#==============================================================================

ENGLISH_DIRECTIONS = {
    "north"    : "north"    , "n" : "north"    ,
    "east"     : "east"     , "e" : "east"     ,
    "south"    : "south"    , "s" : "south"    ,
    "west"     : "west"     , "w" : "west"     ,
    "northeast": "northeast", "ne": "northeast",
    "northwest": "northwest", "nw": "northwest",
    "southeast": "southeast", "se": "southeast",
    "southwest": "southwest", "sw": "southwest",
    "up"       : "up"       , "u" : "up"       ,
    "down"     : "down"     , "d" : "down"     ,
}


ENGLISH_RULES=(
    ("go"         , r"(?:go )?(%s)$" % "|".join(ENGLISH_DIRECTIONS.keys())),
    ("take"       , r"take (\w+)$"),
    ("drop"       , r"drop (\w+)$"),
    ("eat"        , r"eat (\w+)$"),
    ("drink"      , r"drink (\w+)$"),
    ("look"       , r"look$"),
    ("inspect"    , r"(?:look at|look|inspect) (\w+)$"),
    ("open"       , r"open (\w+)$"),
    ("open_with"  , r"open (\w+) (?:with|using) (\w+)$"),
    ("close"      , r"close (\w+)"),
    ("attack"     , r"attack (\w+)$"),
    ("attack_with", r"attack (\w+) (?:with|using) (\w+)$"))
