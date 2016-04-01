from .event import Event4

class TakeEvent(Event3):
    def perform(self):
        self.object.move_to(self.actor)
        self.inform("build") #a faire

    def take_failed(self):
        self.fail()
        self.inform("build.failed")
