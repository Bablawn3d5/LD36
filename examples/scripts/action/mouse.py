import entityx
import math
from _entityx_components import InputResponder, Body, Physics, Stats, b2BodyType, CollisionCategory, Renderable, Sound
from gamemath import vector2
from follower import Follower

Vector2 = vector2.Vector2

class MouseFollower(Follower):
    def __init__(self):
        self.inresponder = self.Component(InputResponder)
        self.body = self.Component(Body)
        self.body.position.x = 240
        self.body.position.y = 240

        self.physics = self.Component(Physics)
        self.physics.bodyType = b2BodyType.DYNAMIC
        self.physics.size.x = 10
        self.physics.size.y = 10
        self.physics.category = CollisionCategory.CATEGORY_16
        self.physics.mask.bits = CollisionCategory.CATEGORY_16
        self.physics.isSensor = True
        self.physics.isBullet = True

        self.stats = self.Component(Stats)
        self.is_clicking = False
        self.click_cooldown = 0.1
        self.current_cooldown = 0
        self.previous_dts = [0] * 20
        self.cur_index = 0

        # HIDES THE BUG WHERE A WHITE BOX RANDOMLY APPEARS
        self.rend = self.Component(Renderable)
        self.rend.font = "./fonts/arial.ttf"
        self.rend.fontString = ""



    def update(self, dt):
        self.is_clicking = False

        mousePos = Vector2(self.inresponder.mousePos)

        cur_pos = Vector2(self.body.position)
        dest_pos = mousePos

        distance_to_travel = math.sqrt(math.pow(dest_pos.get_x() - cur_pos.get_x(), 2) + math.pow(dest_pos.get_y() - cur_pos.get_y(), 2))
        # Average an interpolated DT
        self.previous_dts[self.cur_index] = dt
        self.cur_index += 1
        self.cur_index = self.cur_index % 20
        # If close enough just set speed to 0, else smooth speed to dest
        if(distance_to_travel > 0.05 and dt > 0):
            # Speed = smoothed dt
            new_speed = (distance_to_travel / max(sum(self.previous_dts)/20, 0.016))
            self.stats.speed = new_speed
        else:
            self.stats.speed = 0

        direction_vec = dest_pos - cur_pos
        direction_vec.normalize()
        direction_vec.copy_to(self.body.direction)

        input_events = self.inresponder.responds
        if "+Spawn" in input_events and self.physics.collisionCount > 0:
            self.is_clicking = False
        if "-Spawn" in input_events:
            self.is_clicking = True

        if (self.current_cooldown <= 0):
            if(self.is_clicking):
                # Reset cooldown
                self.current_cooldown = self.click_cooldown
        else:
            self.current_cooldown -= dt;
