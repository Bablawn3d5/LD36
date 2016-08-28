import entityx
import math
from mouse import MouseFollower
from _entityx_components import Renderable, Body, Physics, Stats, b2BodyType, CollisionCategory, Sound
from gamemath import vector2
from follower import Orbital
from spawner import MagicSpawner

Vector2 = vector2.Vector2
TILESIZE_X = 80
TILESIZE_Y = 60


class Button(entityx.Entity):
    def __init__(self):
        self.body = self.Component(Body)
        self.physics = self.Component(Physics)
        self.physics.size.x = TILESIZE_X*3
        self.physics.size.y = TILESIZE_Y*1
        self.physics.category = CollisionCategory.CATEGORY_16
        self.physics.mask.bits = CollisionCategory.CATEGORY_16
        self.rend = self.Component(Renderable)
        self.rend.texture = "./images/button.png"
        self.center = Vector2(self.body.position.x + self.physics.size.x/2,
            self.body.position.y + self.physics.size.y/2)
        self.updated = False
        self.enabled = False
        self.cost_to_click = 0
        self.timer = 0
        self.current_timer = 0

        self.recurring_value = 0
        self.button_text = ButtonText()
        self.button_cost_text = ButtonText()
        self.click_count = 0

    def enable(self):
        if self.enabled == False:
            self.enabled = True

            self.button_text.rend.fontString = self.button_text.rend.base_text + ": 0"
            self.button_text.rend.dirty = True;

            self.button_cost_text.rend.fontString = "Cost: " + str(self.cost_to_click) + " (0 h/s)"
            self.button_cost_text.rend.dirty = True

    def increaseClickCost(self):
        if self.enabled == True:
            self.cost_to_click = self.cost_to_click + 1
            self.button_cost_text.rend.fontString = "Cost: " + str(self.cost_to_click) + " (" + str(round(self.click_count * self.recurring_value / self.timer, 2)) + " h/s)"
            self.button_cost_text.rend.dirty = True

    def update(self, dt):
        self.current_timer += dt
        self.updated = True

class ButtonText(entityx.Entity):
    def __init__(self):
        self.body = self.Component(Body)
        self.rend = self.Component(Renderable)
        self.base_text = ""
        self.updated = False

    def update(self, dt):
        # Do nothing.
        self.updated = True

class ButtonController(entityx.Entity):
    def __init__(self):
        self.body = self.Component(Body)
        self.physics = self.Component(Physics)
        self.center = Vector2(self.body.position.x + self.physics.size.x/2,
            self.body.position.y + self.physics.size.y/2)
        self.init = False
        self.current_score = 0

        self.rend = self.Component(Renderable)
        self.rend.font = "./fonts/arial.ttf"
        self.rend.fontString = "Heat: 0"
        self.rend.r = 78
        self.rend.g = 190
        self.rend.b = 78
        self.rend.a = 190

        self.STICK_COUNT = 10
        self.TREE_COUNT = 10
        self.PEOPLE_COUNT = 10
        self.BUILDING_COUNT = 10
        self.CITY_COUNT = 10
        self.CONTINENT_COUNT = 10
        self.PLANET_COUNT = 10

        self.mouse = MouseFollower()

    def update(self, dt):
        if (self.init == False):
            self.button1 = self.createButton(TILESIZE_X*0,TILESIZE_Y*2, "Sticks", 5, 1, 1, True)
            self.button2 = self.createButton(TILESIZE_X*0,TILESIZE_Y*3, "Trees", 6, 2, 2, False)
            self.button3 = self.createButton(TILESIZE_X*0,TILESIZE_Y*4, "People", 7, 3, 3, False)
            self.button4 = self.createButton(TILESIZE_X*0,TILESIZE_Y*5, "Buildings", 8, 4, 3, False)
            self.button5 = self.createButton(TILESIZE_X*0,TILESIZE_Y*6, "Cities", 9, 5, 5, False)
            self.button6 = self.createButton(TILESIZE_X*0,TILESIZE_Y*7, "Continent", 10, 6, 6, False)
            self.button7 = self.createButton(TILESIZE_X*0,TILESIZE_Y*8, "Planets", 11, 7, 7, False)
            self.button8 = self.createButton(TILESIZE_X*0,TILESIZE_Y*9, "Galaxies", 12, 8, 8, False)
            self.box = entityx.Entity()
            newBody = self.box.Component(Body)
            newBody.position.x = 480
            newBody.position.y = 180
            self.box.Component(Stats)
            newPhysics = self.box.Component(Physics)
            newPhysics.bodyType = b2BodyType.STATIC
            newPhysics.size.x = 80
            newPhysics.size.y = 60
            newPhysics.category = CollisionCategory.CATEGORY_16
            # Colldie with mouse interactables and orbital junk
            newPhysics.mask.bits = CollisionCategory.CATEGORY_16 | CollisionCategory.CATEGORY_15
            newRenderable = self.box.Component(Renderable)
            newRenderable.texture = "./images/FlameOn.png"

            self.spawner = Orbital()
            # HIDES BUG WHERE WHITE BOX APPEARS RANDMMLYD
            rend = self.spawner.Component(Renderable)
            rend.font = "./fonts/arial.ttf"
            rend.fontString = ""
            self.spawner.center = Vector2(newBody.position)
            self.spawner.physics.size.x = 50
            self.spawner.physics.size.y = 50
            self.spawner.r = 200
            self.spawner.totalTime = 5

            self.init = True

        self.process_button(self.button1)
        self.process_button(self.button2)
        self.process_button(self.button3)
        self.process_button(self.button4)
        self.process_button(self.button5)
        self.process_button(self.button6)
        self.process_button(self.button7)
        self.process_button(self.button8)

        if (self.button1.click_count > self.STICK_COUNT):
                self.button2.enable()
        if (self.button2.click_count > self.TREE_COUNT):
                self.button3.enable()
        if (self.button3.click_count > self.PEOPLE_COUNT):
                self.button4.enable()
        if (self.button4.click_count > self.BUILDING_COUNT):
                self.button5.enable()
        if (self.button5.click_count > self.CITY_COUNT):
                self.button6.enable()
        if (self.button6.click_count > self.CONTINENT_COUNT):
                self.button7.enable()
        if (self.button7.click_count > self.PLANET_COUNT):
                self.button8.enable()

        if (self.box in self.mouse.physics.currentCollisions and self.mouse.is_clicking == True):
            self.current_score += 1
            # Make a sound on click
            e = entityx.Entity()
            sound = e.Component(Sound)
            sound.name = "sounds/Explode.wav"

        self.rend.fontString = "Heat: " + str(self.current_score)
        self.rend.dirty = True
        
        if (self.button8.click_count == 100):
            gameOverBox = entityx.Entity()
            newBody = gameOverBox.Component(Body)
            newBody.position.x = 260
            newBody.position.y = 250
            gameOverBox.Component(Stats)
            newPhysics = gameOverBox.Component(Physics)
            newPhysics.bodyType = b2BodyType.STATIC
            newPhysics.size.x = 200
            newPhysics.size.y = 300
            newPhysics.category = CollisionCategory.CATEGORY_1
            newPhysics.mask.bits = CollisionCategory.CATEGORY_1
            newRenderable = gameOverBox.Component(Renderable)
            newRenderable.font = "./fonts/arial.ttf"
            newRenderable.fontSize = 30
            newRenderable.fontString = "You Win!\nFollow us on twitter\n@tehPHEN\n@mitchcraig311"
            newRenderable.r = 186
            newRenderable.g = 26
            newRenderable.b = 119
            

    def process_button(self, button):
        if(button.enabled == True and button.cost_to_click <= self.current_score and button in self.mouse.physics.currentCollisions and self.mouse.is_clicking == True):
            button.click_count = button.click_count + 1
            button.button_text.rend.fontString = button.button_text.rend.base_text + ": " + str(button.click_count)
            button.button_text.rend.dirty = True
            button.button_cost_text.rend.dirty = True
            self.current_score -= button.cost_to_click
            button.increaseClickCost()

            if(button.button_text.rend.base_text == "Sticks"):
                MagicSpawner.spawnStix(Vector2(self.spawner.body.position), self.spawner.center, 50, 250)
            if(button.button_text.rend.base_text == "Trees"):
                MagicSpawner.spawnTree(Vector2(self.spawner.body.position), self.spawner.center, 50, 250)
            if(button.button_text.rend.base_text == "People"):
                MagicSpawner.spawnPeople(Vector2(self.spawner.body.position), self.spawner.center, 50, 250)
            if(button.button_text.rend.base_text == "Buildings"):
                MagicSpawner.spawnBuilding(Vector2(self.spawner.body.position), self.spawner.center, 50, 250)
            if(button.button_text.rend.base_text == "Cities"):
                MagicSpawner.spawnCity(Vector2(self.spawner.body.position), self.spawner.center, 50, 250)
            if(button.button_text.rend.base_text == "Continent"):
                MagicSpawner.spawnContinent(Vector2(self.spawner.body.position), self.spawner.center, 50, 250)
            if(button.button_text.rend.base_text == "Planets"):
                MagicSpawner.spawnPlanet(Vector2(self.spawner.body.position), self.spawner.center, 50, 250)
            if(button.button_text.rend.base_text == "Galaxies"):
                MagicSpawner.spawnGalaxy(Vector2(self.spawner.body.position), self.spawner.center, 50, 250)

            # Make a sound on click
            e = entityx.Entity()
            sound = e.Component(Sound)
            sound.name = "sounds/Explode.wav"
            
        if (button.current_timer >= button.timer):
            button.current_timer = 0
            self.current_score += button.click_count * button.recurring_value


    def createButton(self, x, y, text, cost, value, timer, enabled):

        e = Button()
        e.enabled = enabled
        e.cost_to_click = cost
        e.recurring_value = value
        e.timer = timer

        e.body.position.x = x
        e.body.position.y = y

        e.button_text.body.position.x = x + 15
        e.button_text.body.position.y = y

        e.button_text.rend.font = "./fonts/arial.ttf"
        if (enabled == True):
            e.button_text.rend.fontString = str(text) + ": 0"
        else:
            e.button_text.rend.fontString = "???"
        e.button_text.rend.base_text = str(text)
        e.button_text.rend.r = 78
        e.button_text.rend.g = 190
        e.button_text.rend.b = 78
        e.button_text.rend.a = 190

        e.button_cost_text.body.position.x = x + 15
        e.button_cost_text.body.position.y = y + 32

        e.button_cost_text.rend.font = "./fonts/arial.ttf"
        e.button_cost_text.rend.fontSize = 15
        if (enabled == True):
            e.button_cost_text.rend.fontString = "Cost: " + str(cost) + " (0 h/s)"
        else:
            e.button_cost_text.rend.fontString = ""
        e.button_cost_text.rend.base_text = str(text)
        e.button_cost_text.rend.r = 78
        e.button_cost_text.rend.g = 190
        e.button_cost_text.rend.b = 78
        e.button_cost_text.rend.a = 190

        return e

