import entityx
import math
from mouse import MouseFollower
from _entityx_components import Destroyed, Renderable, Body, Physics, Stats, b2BodyType, CollisionCategory, Sound
from gamemath import vector2
from follower import Orbital
from spawner import MagicSpawner
from eventur import EventController, Event, EVENT_TEXTS

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

    @classmethod
    def increase_sticks(self, obj):
        if obj.click_count < 10:
            return 1
        else:
            return obj.cost_to_click + 1

    def increaseClickCost(self, cost_inc_func = lambda x: x.cost_to_click + 1 ):
        if self.enabled == True:
            self.cost_to_click = cost_inc_func(self)
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

        self.time_count = 0
        self.ending_done = False
        self.ending_start = 0
        self.events_fired = [False] * 100
        self.event_game_ending = False
        self.event_game_done = False

        self.mouse = MouseFollower()

        self.button1 = self.createButton(TILESIZE_X*0,TILESIZE_Y*2, "Sticks", 0, 1, 1, False)
        self.button2 = self.createButton(TILESIZE_X*0,TILESIZE_Y*3, "Trees", 6, 2, 2, False)
        self.button3 = self.createButton(TILESIZE_X*0,TILESIZE_Y*4, "People", 7, 3, 3, False)
        self.button4 = self.createButton(TILESIZE_X*0,TILESIZE_Y*5, "Buildings", 8, 4, 4, False)
        self.button5 = self.createButton(TILESIZE_X*0,TILESIZE_Y*6, "Cities", 9, 5, 5, False)
        self.button6 = self.createButton(TILESIZE_X*0,TILESIZE_Y*7, "Continent", 10, 6, 6, False)
        self.button7 = self.createButton(TILESIZE_X*0,TILESIZE_Y*8, "Planets", 11, 7, 7, False)
        self.button8 = self.createButton(TILESIZE_X*0,TILESIZE_Y*9, "Galaxies", 12, 8, 8, False)

        self.events = EventController()
        newBody = self.events.Component(Body)
        newBody.position.x = 3 * TILESIZE_X + 5
        newBody.position.y = 8 * TILESIZE_Y + 5

    def fireEvent(self, numbah, length = 3, repeat = False):
        if self.events_fired[numbah] == False:
            e = Event(EVENT_TEXTS[numbah+1])
            e.repeat = repeat
            e.event_final = length
            self.events.playEvent(e)
            self.events_fired[numbah] = True

    def update(self, dt):
        self.time_count  += dt
        # FIRE OFF THE INTRODUCTION.
        self.fireEvent(0)
        if (self.time_count >= 4):
            self.fireEvent(1)
        if (self.time_count >= 8):
            self.fireEvent(2)
        if (self.time_count >= 12):
            self.fireEvent(3)
        if (self.time_count >= 16):
            self.fireEvent(4)

        if (self.init == False):
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

        if self.event_game_ending == False:
            self.process_button(self.button1)
            self.process_button(self.button2)
            self.process_button(self.button3)
            self.process_button(self.button4)
            self.process_button(self.button5)
            self.process_button(self.button6)
            self.process_button(self.button7)
            self.process_button(self.button8)

            if (self.box in self.mouse.physics.currentCollisions and self.mouse.is_clicking == True):
                self.current_score += 1
                # Make a sound on click
                e = entityx.Entity()
                e.death = e.Component(Destroyed)
                e.death.timer = 2
                sound = e.Component(Sound)
                sound.name = "sounds/Explode.wav"

        # SCALING LOGIC GOES HERE:
        if(self.current_score > 75 and self.time_count >= 12):
            self.fireEvent(5, length=1.5)

        # Time lock the first unlock
        if(self.current_score > 100 and self.time_count >= 16):
            self.button1.enable()
            self.events.playEvent(Event("The flame draws sticks on its own"))
            self.events.setColor(1)

        if (self.button1.click_count > self.STICK_COUNT):
            self.button2.enable()
            self.events.playEvent(Event("The flame consumes forests alone"))
            self.events.setColor(2)

        if (self.button2.click_count > self.TREE_COUNT):
            self.button3.enable()
            self.events.playEvent(Event("The flame draws once carbon life into it"))
            self.events.setColor(3)

        if (self.button3.click_count > self.PEOPLE_COUNT):
            self.button4.enable()
            self.events.playEvent(Event("The flame grows to consumes homes"))
            self.events.setColor(4)

        if (self.button4.click_count > self.BUILDING_COUNT):
            self.button5.enable()
            self.events.playEvent(Event("Entire cities collapse under the flame"))
            self.events.setColor(5)

        if (self.button5.click_count > self.CITY_COUNT):
            self.button6.enable()
            self.events.playEvent(Event("There is nothing left but masses of land"))
            self.events.setColor(6)

        if (self.button6.click_count > self.CONTINENT_COUNT):
            self.button7.enable()
            self.events.playEvent(Event("The flame pulls planets into its gravity"))
            self.events.setColor(7)

        if (self.button7.click_count > self.PLANET_COUNT):
            self.button8.enable()
            self.events.playEvent(Event("Once distant galaxies are drawn into the flame"))
            self.events.setColor(8)

        if (self.button8.click_count == 100 and self.event_game_done == False):
            self.event_game_ending = True
            self.do_ending(dt)
            if self.ending_done == True and self.event_game_done == False:
                self.do_credits()

        self.rend.fontString = "Heat: " + str(self.current_score)
        self.rend.dirty = True

    def do_ending(self, dt):
        if self.ending_start == 0:
            self.ending_start = self.time_count
            self.ending_score = self.current_score
        heat_loss_time = 45
        self.current_score = int(self.ending_score - self.ending_score*min( heat_loss_time,self.time_count-self.ending_start)/ heat_loss_time)


        self.fireEvent(6, length = 2) # "The flame consumed the entire universe.",
        if (self.time_count >= self.ending_start+4):
            self.fireEvent(7, length = 2) # "There is nothing left to consume.",
        if (self.time_count >= self.ending_start+8):
# "The flame not satisfied.. but theres nothing left",
            self.fireEvent(8, length = 2)
        if (self.time_count >= self.ending_start+12):
# "...",
            self.fireEvent(9, length = 1)
        if (self.time_count >= self.ending_start+16):
# "...",
            self.fireEvent(10, length=5)
        if (self.time_count >= self.ending_start+21):
# "The world once is void of any life.",
            self.fireEvent(11,length=6)
        if (self.time_count >= self.ending_start+28):
# "...",
            self.fireEvent(12,length=1)
        if (self.time_count >= self.ending_start+31):
# "There is only you, in this cold dark room.",
            self.fireEvent(13, length = 8)
        if (self.time_count >= self.ending_start+43):
            # "...",
            self.fireEvent(14, length = 3)
        if (self.time_count >= self.ending_start+46):
# "...",
            self.fireEvent(16, length = 2)
        if (self.time_count >= self.ending_start+50):
# "There is only you, and these sticks.",
            self.fireEvent(17)
        if (self.time_count >= self.ending_start+54):
# "You desire to be reunited with that feeling again...",
            self.fireEvent(18)
        if (self.time_count >= self.ending_start+58):
# "You put some sticks together to start the flame."
            self.fireEvent(19)
        if (self.time_count >= self.ending_start+66):
            self.ending_done = True



    def do_credits(self):
            self.event_game_done = True
            gameOverBox = entityx.Entity()
            newBody = gameOverBox.Component(Body)
            newBody.position.x = 260
            newBody.position.y = 180
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
            newRenderable.fontString ="""The flame continues in our hearts.
      Thank you for playing!
      Follow us on twitter
      @tehPHEN
      @mitchcraig311"""
            newRenderable.r = 255
            newRenderable.g = 244
            newRenderable.b = 255

            e = entityx.Entity()
            sound = e.Component(Sound)
            e.death = e.Component(Destroyed)
            e.death.timer = 2
            sound.name = "sounds/tada.wav"


    def process_button(self, button):
        if(button.enabled == True and button.cost_to_click <= self.current_score and button in self.mouse.physics.currentCollisions and self.mouse.is_clicking == True):
            button.click_count = button.click_count + 1
            button.button_text.rend.fontString = button.button_text.rend.base_text + ": " + str(button.click_count)
            button.button_text.rend.dirty = True
            button.button_cost_text.rend.dirty = True
            self.current_score -= button.cost_to_click

            if(button.button_text.rend.base_text == "Sticks"):
                MagicSpawner.spawnStix(Vector2(self.spawner.body.position), self.spawner.center, 50, 250)
                button.increaseClickCost(Button.increase_sticks)
            if(button.button_text.rend.base_text == "Trees"):
                MagicSpawner.spawnTree(Vector2(self.spawner.body.position), self.spawner.center, 50, 250)
                button.increaseClickCost()
            if(button.button_text.rend.base_text == "People"):
                MagicSpawner.spawnPeople(Vector2(self.spawner.body.position), self.spawner.center, 50, 250)
                button.increaseClickCost()
            if(button.button_text.rend.base_text == "Buildings"):
                MagicSpawner.spawnBuilding(Vector2(self.spawner.body.position), self.spawner.center, 50, 250)
                button.increaseClickCost()
            if(button.button_text.rend.base_text == "Cities"):
                MagicSpawner.spawnCity(Vector2(self.spawner.body.position), self.spawner.center, 50, 250)
                button.increaseClickCost()
            if(button.button_text.rend.base_text == "Continent"):
                MagicSpawner.spawnContinent(Vector2(self.spawner.body.position), self.spawner.center, 50, 250)
                button.increaseClickCost()
            if(button.button_text.rend.base_text == "Planets"):
                MagicSpawner.spawnPlanet(Vector2(self.spawner.body.position), self.spawner.center, 50, 250)
                button.increaseClickCost()
            if(button.button_text.rend.base_text == "Galaxies"):
                MagicSpawner.spawnGalaxy(Vector2(self.spawner.body.position), self.spawner.center, 50, 250)
                button.increaseClickCost()

             # Make a sound on click
            e = entityx.Entity()
            e.death = e.Component(Destroyed)
            e.death.timer = 2
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

