import entityx
from _entityx import Entity
from _entityx_components import Sound, CollisionCategory, Destroyed, Body, Physics, Stats, b2BodyType, Renderable
from gamemath import vector2
import re

Vector2 = vector2.Vector2

# CHARACTER LIMIT IS ROUGHLY 50 CHARS
EVENT_TEXTS = [
"50CHARS50CHARS50CHARS50CHARS50CHARS50CHARS50CHARS",
"You sit in a dark room with only sticks around you.",
"This world is void of any life.",
"There is only you and these sticks...",
"You put some sticks together to start the flame.",
"Kindle the flame, it desires to be bigger.",
"The flame flickers in the dark.",
"You've consumed the entire universe."
]

class Event(object):
    def __init__(self, string):
        self.old_count = 0
        self.event_current = 0
        self.event_final = 3
        self.event_text = string
        self.is_rendering = True
        self.sound_player_prog = re.compile("[AEIOUaeiouYyZzHhMmTtfF.]")

    def play(self,dt):
        if self.is_rendering:
            self.event_current += dt
            if self.event_current >= self.event_final:
                self.is_rendering = False
            percent =  min(1,self.event_current / self.event_final)
            char_disp_count = int(percent * len(self.event_text))
            new_chars = self.event_text[self.old_count:char_disp_count]
            # If there's a character that matches the regex, play a sound
            if self.sound_player_prog.search(new_chars):
                e = entityx.Entity()
                e.death = e.Component(Destroyed)
                e.death.timer = 1
                sound = e.Component(Sound)
                sound.name = "sounds/boop.wav"
            self.old_count = char_disp_count
            return self.event_text[:char_disp_count]
        return self.event_text

class EventController(entityx.Entity):
    def __init__(self):
        self.body = self.Component(Body)
        self.physics = self.Component(Physics)

        self.rend = self.Component(Renderable)
        self.rend.font = "./fonts/arial.ttf"
        self.rend.fontString = ""
        self.rend.fontSize = 24
        self.rend.r = 200
        self.rend.g = 190
        self.rend.b = 180
        self.rend.a = 200

        self.events = [None, None, None]

    def update(self, dt):
        event_line1, event_line2, event_line3 = [""]*3
        if(self.events[0] != None):
            event_line1 = self.events[0].play(dt)
        if(self.events[1] != None):
            event_line2 = self.events[1].play(dt)
        if(self.events[2] != None):
            event_line3 = self.events[2].play(dt)
        self.rend.fontString = "%s\n%s\n%s\n" % (event_line1, event_line2,event_line3)
        self.rend.dirty = True

    def playEvent(self, event):
        if len(self.events) >= 3:
            self.events.pop(0)
        self.events.append(event)

