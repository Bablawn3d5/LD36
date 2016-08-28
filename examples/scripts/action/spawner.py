import entityx
from _entityx_components import CollisionCategory, Body, Renderable, InputResponder, Physics, Stats, b2BodyType
from follower import Follower
from gamemath import vector2

Vector2 = vector2.Vector2

class MagicSpawner():
    @classmethod
    def spawnThing(self, spawn_pos, dest_pos, size, speed):
        # TODO(SMA) : Load from JSON file.
        e = Follower()
        e.dest = dest_pos
        bod = e.Component(Body)
        spawn_pos.copy_to(bod.position)
        phys = e.Component(Physics)
        phys.size.x = size
        phys.size.y = size
        phys.category = CollisionCategory.CATEGORY_15;
        phys.mask.bits = CollisionCategory.CATEGORY_16;
        phys.bodyType = b2BodyType.DYNAMIC

        stats = e.Component(Stats)
        stats.speed = speed
        e.explode.can_explode = True
        return e

    @classmethod
    def spawnStix(self, spawn_pos, dest_pos, size, speed):
        e = self.spawnThing(spawn_pos, dest_pos, size, speed)
        rend = e.Component(Renderable)
        rend.texture = "./images/stick_1.png"

    @classmethod
    def spawnTree(self, spawn_pos, dest_pos, size, speed):
        e = self.spawnThing(spawn_pos, dest_pos, size, speed)
        rend = e.Component(Renderable)
        rend.texture = "./images/stick_1.png"

    @classmethod
    def spawnPeople(self, spawn_pos, dest_pos, size, speed):
        e = self.spawnThing(spawn_pos, dest_pos, size, speed)
        rend = e.Component(Renderable)
        rend.texture = "./images/stick_1.png"

    @classmethod
    def spawnBuilding(self, spawn_pos, dest_pos, size, speed):
        e = self.spawnThing(spawn_pos, dest_pos, size, speed)
        rend = e.Component(Renderable)
        rend.texture = "./images/stick_1.png"

    @classmethod
    def spawnCity(self, spawn_pos, dest_pos, size, speed):
        e = self.spawnThing(spawn_pos, dest_pos, size, speed)
        rend = e.Component(Renderable)
        rend.texture = "./images/stick_1.png"

    @classmethod
    def spawnPlanet(self, spawn_pos, dest_pos, size, speed):
        e = self.spawnThing(spawn_pos, dest_pos, size, speed)
        rend = e.Component(Renderable)
        rend.texture = "./images/stick_1.png"

    @classmethod
    def spawnGalaxy(self, spawn_pos, dest_pos, size, speed):
        e = self.spawnThing(spawn_pos, dest_pos, size, speed)
        rend = e.Component(Renderable)
        rend.texture = "./images/stick_1.png"

    @classmethod
    def spawnContinent(self, spawn_pos, dest_pos, size, speed):
        e = self.spawnThing(spawn_pos, dest_pos, size, speed)
        rend = e.Component(Renderable)
        rend.texture = "./images/stick_1.png"
