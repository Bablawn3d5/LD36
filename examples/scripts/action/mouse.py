import entityx
import math
from _entityx_components import InputResponder, Body, Physics, Stats
from gamemath import vector2
from follower import Follower

Vector2 = vector2.Vector2

class MouseFollower(Follower):
    inresponder = entityx.Component(InputResponder)
    body = entityx.Component(Body)
    physics = entityx.Component(Physics)
    stats = entityx.Component(Stats)
    is_clicking = False
    click_cooldown = 0.1
    current_cooldown = 0

    def update(self, dt):
        mousePos = Vector2(self.inresponder.mousePos)
        #mousePos.copy_to(self.body.position)
        #self.physics.dirty = True
        
        cur_pos = Vector2(self.body.position)
        dest_pos = mousePos

        distance_to_travel = math.sqrt(math.pow(dest_pos.get_x() - cur_pos.get_x(), 2) + math.pow(dest_pos.get_y() - cur_pos.get_y(), 2))
        new_speed = (distance_to_travel / dt) / 50
        self.stats.speed = new_speed
        
        direction_vec = dest_pos - cur_pos
        direction_vec.normalize()
        direction_vec.copy_to(self.body.direction)
        
        input_events = self.inresponder.responds
        if "+Spawn" in input_events and self.physics.collisionCount > 0:
            self.is_clicking = True
        if "-Spawn" in input_events:
            self.is_clicking = False

        if (self.current_cooldown <= 0):
            if(self.is_clicking):
                # Reset cooldown
                print "You clicked!"
                self.current_cooldown = self.click_cooldown
        else:
            self.current_cooldown -= dt;