# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

import os.path, yaml
from mud.world                 import World
from mud.db.transcript         import TranscriptDB
from mud.db.user               import UserDB
from mud.models.mixins.evented import Evented

class Game:

    GAMES_DIR = os.path.join(os.path.dirname(__file__), "games")
    SAVES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".games")

    def yaml_initial_filename(self):
        return os.path.join(self.GAMES_DIR, self.name, "initial.yml")

    def yaml_static_filename(self):
        return os.path.join(self.GAMES_DIR, self.name, "static.yml")

    def yaml_current_filename(self):
        return os.path.join(self.SAVES_DIR, self.name, "current.yml")

    def transcripts_filename(self):
        return os.path.join(self.SAVES_DIR, self.name, "transcripts")

    def users_filename(self):
        return os.path.join(self.SAVES_DIR, self.name, "users")

    def __init__(self, name=None, initial=None, current=None, static=None):
        self.name        = name
        self.world       = World()
        self.static      = {}
        self.transcripts = TranscriptDB(self.transcripts_filename())
        self.users       = UserDB(self.users_filename())
        self._initial    = initial
        self._current    = current
        self._static     = static
        if initial is None:
            self._initial = self.yaml_load(self.yaml_initial_filename())
        if current is None:
            self._current = self.yaml_load(self.yaml_current_filename())
        if static  is None:
            [self._static] = self.yaml_load(self.yaml_static_filename())

    def yaml_load(self, filename):
        try:
            return list(yaml.load_all(open(filename)))
        except FileNotFoundError:
            return ""
    
    def load(self):
        self.users.load()
        self.transcripts.load()
        self.static.update(self._static)
        self.users.create_avatars()
        self.world.load(self._initial, self._current)
        del self._initial
        del self._current
        del self._static

    def save(self):
        contents = self.world.save()
        with open(self.yaml_current_filename(), "w") as stream:
            yaml.dump_all(contents, stream)
        self.transcripts.save()
        self.users.save()

    def start_for_player(self, player):
        init = self.static["start"]
        return self.world[init]

    def reset(self):
        # reset all players
        pass
        # remove all current saves
        pass
