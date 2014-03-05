# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .mixins.identified import Identified
from .mixins.propertied import Propertied
from .mixins.evented    import Evented
from .mixins.named      import Named
from .mixins.composed   import Composed

class Model(Identified, Named, Propertied, Evented, Composed):

    """primitive base class for all models."""

    #--------------------------------------------------------------------------
    # initialization
    #--------------------------------------------------------------------------
    
    def __init__(self, **kargs):
        super().__init__(**kargs)

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
        return False

    def is_location(self):
        return False

    def is_container(self):
        return False

    #--------------------------------------------------------------------------
    # model API
    #--------------------------------------------------------------------------

    def all(self):
        """return an iterator over all things in/at the model."""
        yield from self.parts()
