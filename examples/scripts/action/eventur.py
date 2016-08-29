import entityx
from _entityx import Entity
from _entityx_components import Sound, CollisionCategory, Destroyed, Body, Physics, Stats, b2BodyType, Renderable
from gamemath import vector2
import re
import math

Vector2 = vector2.Vector2

# CHARACTER LIMIT IS ROUGHLY 50 CHARS
EVENT_TEXTS = [
"50CHARS50CHARS50CHARS50CHARS50CHARS50CHARS50CHARS",
# 0->4: Intro, played right away
"You sit alone in a cold dark room.                                        ",
"This world is void of any life.                                    ",
"There is only you, and these sticks.             ",
"You put some sticks together to start the flame.",
"Kindle the flame, it desires to be bigger.",

# 5: After heat level >= 20
"The flame flickers in the dark.",

# 6->12: Plays at the end of game
"The flame consumed the entire universe.",
"There is little left to consume.",
"The flame slowly dies, as the last few items burn.",
"...",
"....       ",
# HACK PAD IT OUT WITH WHITESPACES SO IT DOESN"T PRINT SO DAMM SLOW
"The world is void of any life.                          ",
"...  ",
"There is only you, in this cold dark room.                   ",
"...   ",
"....     ",
"...       ",
"There is only you, and these sticks.",
"You desire to be reunited with that feeling again...",
"You put some sticks together to start the flame. "
]

class Event(object):
    def __eq__(self,other):
        if other is None:
            return False
        return self.event_text == other.event_text

    def __init__(self, string):
        self.repeat = False
        self.old_count = 0
        self.event_current = 0
        self.event_final = 1
        self.event_text = string
        self.is_rendering = True
        self.sound_player_prog = re.compile("[AEIOUaeiouYyZzHhMmTtfF.-]")

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
        self.rainbow_text = False
        self.dt = 0

        self.events_seen = []

    def setColor(self, level):
        self.rainbow_text = False
        if level == 1:
            self.rend.r = 200
            self.rend.g = 170
            self.rend.b = 160
            self.rend.a = 200
        if level == 2:
            self.rend.r = 200
            self.rend.g = 150
            self.rend.b = 130
            self.rend.a = 200
        if level == 3:
            self.rend.r = 210
            self.rend.g = 140
            self.rend.b = 130
            self.rend.a = 200
        if level == 4:
            self.rend.r = 210
            self.rend.g = 130
            self.rend.b = 120
            self.rend.a = 200
        if level == 5:
            self.rend.r = 230
            self.rend.g = 120
            self.rend.b = 100
            self.rend.a = 200
        if level == 6:
            self.rend.r = 230
            self.rend.g = 110
            self.rend.b = 95
            self.rend.a = 200
        if level == 7:
            self.rend.r = 230
            self.rend.g = 90
            self.rend.b = 70
            self.rend.a = 200
        if level == 8:
            self.rend.r = 230
            self.rend.g = 90
            self.rend.b = 70
            self.rend.a = 200
            self.rainbow_text = True

    def update(self, dt):
        event_line1, event_line2, event_line3 = [""]*3
        if(self.events[0] != None):
            event_line1 = self.events[0].play(dt)
        if(self.events[1] != None):
            event_line2 = self.events[1].play(dt)
        if(self.events[2] != None):
            event_line3 = self.events[2].play(dt)
        self.rend.fontString = "%s\n%s\n%s\n" % (event_line1, event_line2,event_line3)
        if self.rainbow_text:
            self.dt += min(0.00055,dt)
            cur = self.dt * math.pi
            self.rend.r = max( 20, int(abs(255 * math.sin(cur)) + 20) )
            self.rend.g = max( 0, int(abs(255 * (math.sin(cur/2)))) )
            self.rend.b = max( 5, int(abs(255 * math.cos(cur)) + 20) )

        self.rend.dirty = True

    def flushEvents(self):
        self.events = [None, None, None]

    def playEvent(self, event):
        if event.repeat == False and event in self.events_seen:
            return
        try:
            none_index = self.events.index(None)
            self.events[none_index]=event
        except ValueError:
            self.events.pop(0)
            self.events.append(event)
        self.events_seen.append(event)

