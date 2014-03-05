# -*- coding: utf-8 -*-
# Copyright (C) 2014 Denys Duchier, IUT d'Orléans
#==============================================================================

from tornado.template import Template
from mud.models.mixins.evented import Evented
from mud.models.mixins.propertied import Propertied
import mud.static, re
STATIC = Evented(events=mud.static.STATIC["events"])


class Event(Evented, Propertied):

    NAME = None

    def __init__(self):
        super().__init__()
        self._effects_executed = False

    def execute(self):
        self.perform()
        self.execute_effects()

    def perform(self):
        raise NotImplemented()

    def execute_effects(self):
        if not self._effects_executed:
            self._effects_executed = True
            for effect in self.get_effects(self.NAME):
                effect.execute()

    def format(self, template, **kargs):
        context = self.context()
        context.update(kargs)
        return Template(template).generate(**context).decode()

    def to_html(self, text):
        text = text.strip()
        if not text or text[0]=="<":
            return text
        text = re.sub(r"(?:(?:^|\n)\s*){2,}", r"\n\n", text)
        html = ["<p>%s</p>" % s for s in text.split(r"\n\n")]
        return "\n".join(html)

    def buffer_clear(self):
        self.HTML = []

    def buffer_append(self, html):
        self.HTML.append(html)

    def buffer_htmlize(self, text):
        if not text:
            return
        text = text.strip()
        if not text or text[0]=="<":
            return self.buffer_append(text)
        text = re.sub(r"(?:(?:^|\n)\s*){2,}", r"\n\n", text)
        for item in text.split(r"\n\n"):
            self.buffer_append("<p>%s</p>" % item)

    def buffer_inform(self, dotpath, **kargs):
        text = self.get_template(dotpath)
        if text:
            html = self.format(text, **kargs)
            self.buffer_htmlize(html)

    def buffer_get(self):
        try:
            return "\n".join(self.HTML)
        finally:
            self.buffer_clear()

    def buffer_peek(self, what, **kargs):
        text = what.get_template("info.actor")
        if text:
            html = self.format(text, peeked=what, **kargs)
            self.buffer_append("<li>")
            self.buffer_htmlize(html)
            self.buffer_append("</li>")


class Event1(Event):

    def __init__(self, actor):
        Event.__init__(self)
        self.actor = actor

    def context(self):
        context = super().context()
        context["actor"] = self.actor
        return context

    def observers(self):
        for x in self.actor.container().contents():
            if x is not self.actor and x.is_player() and x.can_see():
                yield x

    def inform(self, dotpath, **kargs):
        self.buffer_clear()
        self.buffer_inform(dotpath+".actor")
        html = self.buffer_get()
        if html:
            self.actor.send_result(html)
        for observer in self.observers():
            self.buffer_clear()
            self.buffer_inform(dotpath+".observer", observer=observer)
            html = self.buffer_get()
            if html:
                observer.send_info(html)
                      

class Event2(Event1):

    def __init__(self, actor, object):
        Event1.__init__(self, actor)
        self.object = object

    def context(self):
        context = super().context()
        context["object"] = self.object
        return context

    def get_event_templates(self):
        return self.object.get_event_templates()


class Event3(Event2):

    def __init__(self, actor, object, object2):
        Event2.__init__(self, actor, object)
        self.object2 = object2

    def context(self):
        context = super().context()
        context["object2"] = self.object2
        return context
