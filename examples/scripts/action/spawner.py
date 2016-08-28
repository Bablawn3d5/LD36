import entityx
from _entityx_components import CollisionCategory, Body, Renderable, InputResponder, Physics, Stats, b2BodyType
from follower import Follower, OrbitalToCenter
from gamemath import vector2
from random import randint, uniform

Vector2 = vector2.Vector2

class MagicSpawner():
    @classmethod
    def spawnThing(self, spawn_pos, dest_pos, size, speed):
        # TODO(SMA) : Load from JSON file.
        e = OrbitalToCenter()
        e.center = dest_pos
        e.r = (spawn_pos - dest_pos).get_magnitude()
        e.s = uniform(0.5,2.5)
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
        rend.texture = "./images/stick_%d.png" % (randint(1,2))

    @classmethod
    def spawnTree(self, spawn_pos, dest_pos, size, speed):
        e = self.spawnThing(spawn_pos, dest_pos, size, speed)
        rend = e.Component(Renderable)
        rend.texture = "./images/tree_%d.png" % (randint(1,1))

    @classmethod
    def spawnPeople(self, spawn_pos, dest_pos, size, speed):
        e = self.spawnThing(spawn_pos, dest_pos, size, speed)
        rend = e.Component(Renderable)
        rend.texture = "./images/person_%d.png" % (randint(1,1))

    @classmethod
    def spawnBuilding(self, spawn_pos, dest_pos, size, speed):
        e = self.spawnThing(spawn_pos, dest_pos, size, speed)
        rend = e.Component(Renderable)
        rend.texture = "./images/house_%d.png" % (randint(1,1))

    @classmethod
    def spawnCity(self, spawn_pos, dest_pos, size, speed):
        e = self.spawnThing(spawn_pos, dest_pos, size, speed)
        rend = e.Component(Renderable)
        rend.texture = "./images/city_%d.png" % (randint(1,1))

    @classmethod
    def spawnPlanet(self, spawn_pos, dest_pos, size, speed):
        e = self.spawnThing(spawn_pos, dest_pos, size, speed)
        rend = e.Component(Renderable)
        rend.texture = "./images/planet_%d.png" % (randint(1,6))

    @classmethod
    def spawnGalaxy(self, spawn_pos, dest_pos, size, speed):
        e = self.spawnThing(spawn_pos, dest_pos, size, speed)
        rend = e.Component(Renderable)
        rend.texture = "./images/galaxy_%d.png" % (randint(1,3))

    @classmethod
    def spawnContinent(self, spawn_pos, dest_pos, size, speed):
        e = self.spawnThing(spawn_pos, dest_pos, size, speed)
        rend = e.Component(Renderable)
        rend.texture = "./images/content_%d.png" % (randint(1,10))
