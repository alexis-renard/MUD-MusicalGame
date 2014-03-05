# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

import os.path

class World:

    DATADIR      = os.path.dirname(__file__)
    YAML_INITIAL = os.path.join(DATADIR, "initial.yml")
    YAML_CURRENT = os.path.join(DATADIR, "current.yml")

    def __init__(self):
        self.database = {}
        self.types    = {}
        #self.load()

    def load_models(self):
        import mud.models as models
        Model = models.Model
        for k,v in models.__dict__.items():
            if not k.startswith("_") and type(v) is type and issubclass(v, Model):
                self.types[v.__name__] = v

    def make(self, data):
        cls = self.types[data["type"]]
        obj = cls(**data)                 # autoadded to database
        obj.yaml = data
        if "id" not in data:
            data["id"] = obj.id
        return obj

    def load(self):
        from yaml import load_all

        self.load_models()
        self.autocreated = []

        # create all objects in the world (except players)
        with open(self.YAML_INITIAL) as stream:
            contents = load_all(stream)
            for data in contents:
                obj = self.make(data)

        # initialize them with the initial yaml data
        for obj in tuple(self.database.values()):
            obj.init_from_yaml(obj.yaml, self)

        # initialize autocreated objects with their yaml data
        while self.autocreated:
            objs = self.autocreated
            self.autocreated = []
            for obj in objs:
                obj.init_from_yaml(obj.yaml, self)

        # update them with the saved current state of the game
        if os.path.exists(self.YAML_CURRENT):
            with open(self.YAML_CURRENT) as stream:
                for data in load_all(stream):
                    key = data["id"]
                    obj = self.database[key]
                    obj.update_from_yaml(data, world)

    def save(self):
        from yaml import dump_all

        contents = [x.to_json() for x in self.database.values()]
        with open(self.YAML_CURRENT, "w") as stream:
            dump_all(contents, stream)

    def __getitem__(self, id):
        return self.database[id]

    def __setitem__(self, id, val):
        self.database[id] = val

    def get(self, key, default=None):
        return self.database.get(key, default)


WORLD = World()
