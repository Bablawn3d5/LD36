import entityx
from _entityx_components import InputResponder, Body, Physics
from gamemath import vector2
from follower import Follower

Vector2 = vector2.Vector2

class MouseFollower(Follower):
    inresponder = entityx.Component(InputResponder)
    body = entityx.Component(Body)
    physics = entityx.Component(Physics)

    def update(self, dt):
        mousePos = Vector2(self.inresponder.mousePos)
        mousePos.copy_to(self.body.position)
        self.physics.dirty = True
