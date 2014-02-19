# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from mud.models.mixins.propertied import Propertied

class Effect(Propertied):

    def __init__(self, yaml, context):
        self.yaml = yaml
        self.context = context

    def context(self):
        return self.context

    def resolve(self, key):
        val = self.yaml.get(key)
        if val is None:
            return self.context[key]
        if val[0] == "*":
            from mud.world import WORLD
            return WORLD[val[1:]]
        return self.context[val]

    @staticmethod
    def make_effect(yaml, context):
        cls = yaml["type"]
        import mud.effects
        cls = mud.effects.__dict__[cls]
        return cls(yaml, context)

    @staticmethod
    def make_effects(yamls, context):
        if not yamls:
            return
        if not isinstance(yamls, list):
            yamls = [yamls]
        for yaml in yamls:
            effect = Effect.make_effect(yaml, context)
            props = yaml.get("props")
            if props is None or effect.has_props(props, context):
                yield effect

    def execute(self):
        raise NotImplemented()


class Effect1(Effect):

    def __init__(self, yaml, context):
        super().__init__(yaml, context)
        self.actor = self.resolve("actor")

    def execute(self):
        self.EVENT(self.actor).execute()


class Effect2(Effect1):

    def __init__(self, yaml, context):
        super().__init__(yaml, context)
        self.object = self.resolve("object")

    def execute(self):
        self.EVENT(self.actor, self.object).execute()


class Effect3(Effect2):

    def __init__(self, yaml, context):
        super().__init__(yaml, context)
        self.object2 = self.resolve("object2")

    def execute(self):
        self.EVENT(self.actor, self.object, self.object2).execute()
