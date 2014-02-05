# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .model import Model

class Portal(Model):

    """a Portal has 2 exits.  Each exit is located at a certain location in a
    given direction.  An exit refers to the properties of its portal.  In YAML
    a portal is described by:

    type: portal
    props: [closable, closed]
    exits:
      - location: dark-cave
        direction: north
        long:
          - true: [closed]
            text: north is a wooden door
          - false:[closed]
            text: |
              north is wooden door.  it is ajar and leads into
              a dark cave.
      - location: treasure-room
        direction: south
        long:
          - true: [closed]
            text: north, a heavy boulder blocks a passage
          - false:[closed]
            text: |
              north, a boulder has been rolled to the side. there
              is a passage leading into a brightly lit treasure room.
    """

    #--------------------------------------------------------------------------
    # initialization
    #--------------------------------------------------------------------------

    def __init__(self, **kargs):
        super().__init__(**kargs)
        self.exits = []

    #--------------------------------------------------------------------------
    # initialization from YAML data
    #--------------------------------------------------------------------------

    def init_from_yaml(self, data, world):
        super().init_from_yaml(data, world)
        for edata in data["exits"]:
            if "type" not in edata:
                edata["type"] = "Exit"
            obj = world.make(edata)
            obj.portal = self
            self.exits.append(obj)
            world.autocreated.append(obj)

    def update_from_yaml(self, data, world):
        super().update_from_yaml(data, world)

    #--------------------------------------------------------------------------
    # API for saving the dynamic part of objects to YAML (via JSON)
    #--------------------------------------------------------------------------

    def archive_into(self, obj):
        super().archive_into(obj)
