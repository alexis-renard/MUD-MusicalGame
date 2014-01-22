# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from mud.db.transcript import DATABASE as TRANSCRIPTS

class Player:

    PLAYERS = {}

    def __new__(cls, username):
        player = cls.PLAYERS.get(username, None)
        if player is not None:
            return player
        return super(Player, cls).__new__(cls)

    def __init__(self, username):
        if hasattr(self, "username"): # check if the player has already been initialized
            return                    # in which case, nothing more needs to be done
        self.username = username      # otherwise, add the appropriate attributes
        self.transcript = TRANSCRIPTS.lookup(username)

    def __str__(self):
        return self.username
