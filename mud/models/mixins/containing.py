# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .propertied import Propertied

class Containing(Propertied):

    """a mixin that provides the ability to have content."""

    #--------------------------------------------------------------------------
    # initialization
    #--------------------------------------------------------------------------

    def __init__(self, **kargs):
        super().__init__(**kargs)
        self._contents = set()

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
    # contents API
    #--------------------------------------------------------------------------

    def contents(self):
        """return an iterator over the contents of the container."""
        return iter(self._contents)

    def add(self, obj):
        """add an object or player to the container."""
        self._contents.add(obj)

    def remove(self, obj):
        """remove an object or player from the container."""
        self._contents.remove(obj)


    #--------------------------------------------------------------------------
    # FIXME!!!
    #--------------------------------------------------------------------------

    def long_description_for(self, player):
        # if the player cannot see, then return a short description
        # which hopefully takes into account the fact that the player
        # cannot see and says something like "it is pitch dark here. you
        # cannot see anything."
        if not player.can_see(self):
            return self.dark_description()
        text = self.long_description().strip()
        text = EMPTY_LINE.sub("\n", text)
        if not text.startswith("<"):
            text = "\n".join(("<p>%s</p>" % t) for t in text.split())
        things = []
        for x in self:
            things.append("<li>%s</li>" % x.short_description())
        text += "<ul>%s</ul>" % "\n".join(things)
        return text

    def dark_description(self):
        return "<p>il fait sombre ici... on n'y voit rien!</p>"

    def short_description_for(self, player):
        if not player.can_see(self):
            return self.dark_description()
        text = self.short_description().strip()
        text = EMPTY_LINE.sub("\n", text)
        if not text.startswith("<"):
            text = "\n".join(("<p>%s</p>" % t) for t in text.split())
        return text

