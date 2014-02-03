# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .action import Action2

class Go(Action2):

    def perform(self):
        e = self.arg1.container().find_exit(self.arg2)
        if e is None:
            # no such exit
            # send back a message, then
            return
        if not e.is_open():
            # move not possible
            # the exit should have a method for constructing
            # the appropriate message
            e.go_failed(self.arg1)
            return
        # move is possible
        # the exit might have a method for constructing an
        # appropriate message describing the move
        e.go_succeeded(self.arg1)
        # actually move the player
        self.arg1.move_to(e.destination())
        # construct a message describing where the player
        # lands. maybe it should be the other exit that is
        # in charge of providing such descriptions. other
        # players should be informed.
        e.destination().arrival(self.arg1)

