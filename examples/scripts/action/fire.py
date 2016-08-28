import entityx
from _entityx_components import Renderable, Body, Physics
from gamemath import vector2

Vector2 = vector2.Vector2

class Flicker(entityx.Entity):
    def __init__(self):
        self.body = self.Component(Body)
        self.physics = self.Component(Physics)
        self.renderable = self.Component(Renderable)
        self.x = 1
        self.y = 1
        self.size = Vector2(self.physics.size.x, self.physics.size.y)
        self.center = Vector2(self.body.position.x + self.physics.size.x/2,
            self.body.position.y + self.physics.size.y/2)
        self.dest = None

    def update(self, dt):
        scalefactor = (0.05+dt*10)
        self.physics.size.x = int(scalefactor*self.size.x)
        self.physics.size.y = int(scalefactor*self.size.y)
        self.renderable.scale.x = self.x+scalefactor
        self.renderable.scale.y = self.y+scalefactor
        # HACK(SMA):  I CAN"T MATH ADD 50 RANDOMLYAAAAAAA
        self.body.position.x = self.center.x + (self.physics.size.x/2*scalefactor) - 20*(1+scalefactor)
        self.body.position.y = self.center.y + (self.physics.size.y/2*scalefactor) - 20*(1+scalefactor)
        self.physics.dirty = True


