# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

class Action:

    def execute(self):
        if self.arg1.is_alive():
            self.perform()

    def perform(self):
        raise NotImplemented()

class Action1(Action):

    def __init__(self, subject):
        self.arg1 = subject

class Action2(Action1):

    def __init__(self, subject, object):
        Action1.__init__(self, subject)
        self.arg2 = object

class Action3(Action2):

    def __init__(self, subject, object, object2):
        Action2.__init__(self, subject, object)
        self.arg3 = object2
