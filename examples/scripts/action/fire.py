import entityx
from _entityx_components import Renderable, Body, Physics
from gamemath import vector2

Vector2 = vector2.Vector2

class Flicker(entityx.Entity):
    def __init__(self):
        self.body = self.Component(Body)
        self.x = 1
        self.y = 1
        self.renderable = self.Component(Renderable)
        self.size = Vector2(80, 60)
        self.center = Vector2(self.body.position.x + self.size.x/2,
            self.body.position.y + self.size.y/2)


    def update(self, dt):
        scalefactor = (0.05+dt*10)
        self.renderable.scale.x = self.x+scalefactor
        self.renderable.scale.y = self.y+scalefactor
        # HACK(SMA):  I CAN"T MATH ADD 50 RANDOMLYAAAAAAA
        self.body.position.x = self.center.x + (self.size.x/2*scalefactor) - 20*(1+scalefactor)
        self.body.position.y = self.center.y + (self.size.y/2*scalefactor) - 20*(1+scalefactor)


