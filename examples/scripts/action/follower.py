import entityx
from _entityx_components import Body, Physics, Stats, Destroyed
from explosion import Exploder, Explodes
from gamemath import vector2
import math

Vector2 = vector2.Vector2

class Follower(entityx.Entity):
    def __init__(self):
        self.body = self.Component(Body)
        self.physics = self.Component(Physics)
        self.stats = self.Component(Stats)
        self.explode = Explodes()
        self.dest = None

    def update(self, dt):
        cur_pos = Vector2(self.body.position)
        dest_pos = self.dest

        direction_vec = dest_pos - cur_pos
        direction_vec.normalize()

        next_pos = Vector2()
        next_pos.set_x(cur_pos.get_x() + self.stats.speed * dt)
        next_pos.set_y(cur_pos.get_y() + self.stats.speed * dt)

        next_direction_vec = dest_pos - next_pos
        next_direction_vec.normalize()

        if(abs(direction_vec.get_x() + next_direction_vec.get_x()) > 1.0 or abs(direction_vec.get_y() + next_direction_vec.get_y()) > 1.0):
            # We haven't passed our destination in the next frame, so keep on course
            direction_vec.copy_to(self.body.direction)
        else:
            direction_vec.set_x(0)
            direction_vec.set_y(0)
            direction_vec.copy_to(self.body.direction)
            dest_pos.copy_to(self.body.position)

        Exploder.check_explodes(self, dt)


class Orbital(entityx.Entity):
    def __init__(self):
        self.body = self.Component(Body)
        self.physics = self.Component(Physics)
        self.stats = self.Component(Stats)
        self.center = Vector2()
        self.r = 1
        self.cur_dt = 0
        self.totalTime = 1.0

    def update(self, dt):
        self.cur_dt += dt
        self.body.position.x = self.center.x + self.r * math.sin( (self.cur_dt/self.totalTime) * 2*math.pi)
        self.body.position.y = self.center.y + self.r * math.cos( (self.cur_dt/self.totalTime) * 2*math.pi)
        if (self.cur_dt >= self.totalTime):
            self.cur_dt = 0
        self.physics.dirty = True


class OrbitalToCenter(entityx.Entity):
    def __init__(self):
        self.body = self.Component(Body)
        self.physics = self.Component(Physics)
        self.stats = self.Component(Stats)
        self.center = Vector2()
        self.s = 1.0
        self.r = 1
        self.cur_dt = 0
        self.totalTime = 1.0
        self.explode = Explodes()
        self.death = self.Component(Destroyed)
        self.death.timer = 25

    def update(self, dt):
        self.cur_dt += dt
        percent = (self.cur_dt/self.totalTime)
        self.body.position.x = self.center.x + self.r * (1-percent) * math.sin( self.s*math.pi + percent * 2*math.pi)
        self.body.position.y = self.center.y + self.r * (1-percent) * math.cos( self.s*math.pi + percent * 2*math.pi)
        if (self.cur_dt >= self.totalTime):
            self.cur_dt = 0
        self.physics.dirty = True
        Exploder.check_explodes(self, dt)
