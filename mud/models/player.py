# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from mud.db.transcript import DATABASE as TRANSCRIPTS
from .thing      import Thing
from .containing import Containing

class Player(Containing, Thing):

    _UUID_IF_ID_MISSING = True
    _PLAYERS = {}

    def __new__(cls, name=None, **kargs):
        player = cls._PLAYERS.get(name, None)
        if player is not None:
            return player
        return super(Player, cls).__new__(cls)

    #--------------------------------------------------------------------------
    # initialization
    #--------------------------------------------------------------------------

    def __init__(self, name=None, **kargs):
        if hasattr(self, "name"):     # check if the player has already been initialized
            return                    # in which case, nothing more needs to be done
        super().__init__(**kargs)     # otherwise, initialize base classes
        _PLAYERS[name]  = self        # save player in static dict
        self.transcript = TRANSCRIPTS.lookup(name) # and add appropriate attributes

    #--------------------------------------------------------------------------
    # initialization from YAML data
    #--------------------------------------------------------------------------

    def init_from_yaml(self, data, world):
        super().init_from_yaml(data, world)

    def update_from_yaml(self, data, world):
        super().update_from_yaml(data, world)

    #--------------------------------------------------------------------------
    # API for saving the dynamic part of objects to YAML (via JSON)
    #--------------------------------------------------------------------------

    def archive_into(self, obj):
        super().archive_into(obj)

    #--------------------------------------------------------------------------
    # type tests for general categories of models
    #--------------------------------------------------------------------------

    def is_player(self):
        return True

    #--------------------------------------------------------------------------
    # model API
    #--------------------------------------------------------------------------

    def __str__(self):
        return self.name

    def find_in_context(self, name):
        """return the object in the player's inventory or present at his
        location and identified by this name, or None if no such object
        is found."""
        return self.find(name) or \
            (self.container and self.container.find(name))

    #--------------------------------------------------------------------------
    # API for sending messages back to the user through his websocket
    #--------------------------------------------------------------------------

    def _send(self, msg):
        ws = getattr(self, "websocket", None)
        if ws:
            ws.write_message(msg)

    def send_echo(self, html):
        """sends back the commands as received."""
        self._send({"type": "echo", "html": html})

    def send_error(self, html):
        """sends an error message for a command that was not understood
        or could not be executed."""
        self._send({"type": "error", "html": html})

    def send_result(self, html):
        """sends a description that is a consequence from the user's last
        action."""
        self._send({"type": "result", "html": html})

    def send_info(self, html):
        """sends a description for an event not initiated by the user.
        for example, for actions of players in the same location."""
        self._send({"type": "info", "html": html})
