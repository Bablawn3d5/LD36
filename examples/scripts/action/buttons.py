import entityx
from mouse import MouseFollower
from _entityx_components import Renderable, Body, Physics, Stats, b2BodyType, CollisionCategory
from gamemath import vector2

Vector2 = vector2.Vector2
TILESIZE_X = 80
TILESIZE_Y = 60


class Button(entityx.Entity):
    def __init__(self):
        self.body = self.Component(Body)
        self.physics = self.Component(Physics)
        self.physics.size.x = TILESIZE_X*3
        self.physics.size.y = TILESIZE_Y*1
        self.rend = self.Component(Renderable)
        self.rend.texture = "./images/button.png"
        self.center = Vector2(self.body.position.x + self.physics.size.x/2,
            self.body.position.y + self.physics.size.y/2)
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
        self.rend.fontString = "Score: 0"
        self.rend.r = 78
        self.rend.g = 190
        self.rend.b = 78
        self.rend.a = 190
        
        self.mouse = MouseFollower()

    def update(self, dt):
        if (self.init == False):
            self.button1 = self.createButton(TILESIZE_X*0,TILESIZE_Y*2)
            self.button2 = self.createButton(TILESIZE_X*0,TILESIZE_Y*3)
            self.button3 = self.createButton(TILESIZE_X*0,TILESIZE_Y*4)
            self.button4 = self.createButton(TILESIZE_X*0,TILESIZE_Y*5)
            self.button5 = self.createButton(TILESIZE_X*0,TILESIZE_Y*6)
            self.button6 = self.createButton(TILESIZE_X*0,TILESIZE_Y*7)
            self.button7 = self.createButton(TILESIZE_X*0,TILESIZE_Y*8)
            self.button8 = self.createButton(TILESIZE_X*0,TILESIZE_Y*9)
            
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
            newPhysics.mask.bits = CollisionCategory.CATEGORY_16
            newRenderable = self.box.Component(Renderable)
            newRenderable.texture = "./images/FlameOn.png"
            
            self.init = True
            
        if (self.box in self.mouse.physics.currentCollisions and self.mouse.is_clicking == True):
            self.current_score = self.current_score + 1
            self.rend.fontString = "Score: " + str(self.current_score)
            self.rend.dirty = True

    def createButton(self, x, y):
        e = Button()
        e.body.position.x = x
        e.body.position.y = y
        return e

