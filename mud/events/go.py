# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from .event import Event2


class EnterPortalEvent(Event2):

    @property
    def exit(self):
        return self.object

    def perform(self):
        self.traversal = self.exit.get_traversal()
        if not self.actor.can_pass(self.traversal.exit1):
            self.add_prop("cannot-pass")
            self.add_prop("cannot-pass-exit1")
            return self.enter_portal_failure()
        if not self.actor.can_pass(self.traversal.exit2):
            self.add_prop("cannot-pass")
            self.add_prop("cannot-pass-exit2")
            return self.enter_portal_failure()
        self.enter_portal_success()
        self.execute_effects()
        TraversePortalEvent(self.actor, self.traversal).execute()

    def enter_portal_success(self):
        self.inform("enter-portal")

    def enter_portal_failure(self):
        self.inform("enter-portal.failed")

    def context(self):
        context = super().context()
        context["exit"] = self.exit


class TraversePortalEvent(Event2):

    @property
    def traversal(self):
        return self.object

    def perform(self):
        self.inform("traverse-portal")
        self.traversal.commit()
        self.actor.move_to(self.traversal.exit2.location)
        self.execute_effects()
        LeavePortalEvent(self.actor, self.traversal.exit2).execute()

    def context(self):
        context = super().context()
        context["traversal"] = self.traversal


class LeavePortalEvent(Event2):

    @property
    def exit(self):
        return self.object

    def perform(self):
        self.inform("leave-portal")

    def context(self):
        context = super().context()
        context["exit"] = self.exit
