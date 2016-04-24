# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================
#
# from .action                      import Action2
# from mud.events                   import TeleportEvent
# from mud.models.mixins.containing import Containing
# from mud.models                   import Player
# import mud.game

# class TeleportAction(Action2):
#
#     def __init__(self, subject, o, object2):
#
#         Action2.__init__(self, subject, object2)
#         self.object2 = o
#         self.object2_resolved = None
#
#     EVENT = TeleportEvent
#     ACTION = "teleport"
#
#     def resolve_object(self):
#         world = mud.game.GAME.world
#         loc = world.get(self.object)
#         if loc:
#             locs = [loc]
#         else:
#             locs = []
#             for k,v in world.items():
#                 if isinstance(v, Containing) and \
#                    not isinstance(v, Player) and \
#                    k.find(self.object) != -1:
#                     locs.append(v)
#         return locs


from .action import Action3
from mud.events import PlayWithEvent


class PlayWithAction(Action3):
    # instrument = self.resolve_object2()
    # partition = self.resolve_object()
    EVENT = PlayWithEvent
    RESOLVE_OBJECT = "resolve_for_operate"
    RESOLVE_OBJECT2 = "resolve_for_use"
    ACTION = "play-with"

    # NAME = "teleport"
    #
    # def perform(self):
    #     n = len(self.object)
    #     if n == 0:
    #         self.fail()
    #         self.inform("teleport.not-found")
    #     elif n > 1:
    #         self.fail()
    #         self.inform("teleport.ambiguous")
    #     else:
    #         self.inform("teleport.departure")
    #         self.actor.move_to(self.object[0])
    #         self.inform("teleport.arrival")
    #         InfoEvent(self.actor).execute()

    # if instrument.has_prop("playable"):
    #     loc = instrument._getprops()[0] #les id des locations seront tjrs en première position dans la liste (ordre défini dans le yaml)
    #
    # else:



    # EVENT = TeleportEvent
    # ACTION = "teleport"
    #
    # def resolve_object(self):
    #     world = mud.game.GAME.world
    #     loc = world.get(self.object)
    #     if loc:
    #         locs = [loc]
    #     else:
    #         locs = []
    #         for k,v in world.items():
    #             if isinstance(v, Containing) and \
    #                not isinstance(v, Player) and \
    #                k.find(self.object) != -1:
    #                 locs.append(v)
    #     return locs
