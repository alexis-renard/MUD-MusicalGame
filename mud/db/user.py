# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from mud.db.basic import BasicDB

class UserDB(BasicDB):

    def authenticate(self, username, password):
        with self.lock:
            user = self.get(username, None)
            return user and user["password"]==password

    def create_user(self, username, password):
        with self.lock:
            if username in self:
                return None
            user = {
                "username": username,
                "password": password,
            }
            self[username] = user
            self.save()
            return user

    def create_avatars(self):
        from mud.models.player import Player
        with self.lock:
            for username in self:
                Player(username)
