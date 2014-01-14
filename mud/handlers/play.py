# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from mud.handlers.base import BaseHandler
from mud.db.transcript import DATABASE as TRANSCRIPTS

#==============================================================================
# play handler
#==============================================================================

class PlayHandler(BaseHandler):

    def extras(self):
        return {
            "messages": TRANSCRIPTS.lookup(self.get_current_user())
        }

    @tornado.web.authenticated
    def post(self):
        user = self.get_current_user()
        
